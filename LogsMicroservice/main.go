package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

// MongoDB configuration
var mongoClient *mongo.Client
var logsCollection *mongo.Collection

func initMongoDB() {
	// Load environment variables
	err := godotenv.Load(".env")
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	mongoURI := os.Getenv("MONGO_URI")
	dbName := os.Getenv("DB_NAME")
	collectionName := os.Getenv("COLLECTION_NAME")

	// Connect to MongoDB
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	client, err := mongo.Connect(ctx, options.Client().ApplyURI(mongoURI))
	if err != nil {
		log.Fatalf("Error connecting to MongoDB: %v", err)
	}

	// Test the connection
	err = client.Ping(ctx, nil)
	if err != nil {
		log.Fatalf("Error pinging MongoDB: %v", err)
	}

	log.Println("Conexión a MongoDB exitosa.")
	mongoClient = client
	logsCollection = client.Database(dbName).Collection(collectionName)
}

func saveLog(c *gin.Context) {
	var requestBody struct {
		Email string                 `json:"email" binding:"required"`
		Log   map[string]interface{} `json:"log" binding:"required"`
	}

	if err := c.ShouldBindJSON(&requestBody); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	// Find or create user document
	filter := bson.M{"email": requestBody.Email}
	update := bson.M{
		"$push": bson.M{"logs": requestBody.Log},
	}
	opts := options.Update().SetUpsert(true)

	_, err := logsCollection.UpdateOne(ctx, filter, update, opts)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al guardar el log en MongoDB"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Log guardado exitosamente"})
}

func getAllLogs(c *gin.Context) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	cursor, err := logsCollection.Find(ctx, bson.D{})
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al recuperar los logs"})
		return
	}
	defer cursor.Close(ctx)

	var results []bson.M
	if err := cursor.All(ctx, &results); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al procesar los logs"})
		return
	}

	c.JSON(http.StatusOK, results)
}

func getLogsByEmail(c *gin.Context) {
	email := c.Param("email")

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	var userLogs bson.M
	err := logsCollection.FindOne(ctx, bson.M{"email": email}).Decode(&userLogs)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Usuario no encontrado"})
		return
	}

	c.JSON(http.StatusOK, userLogs)
}

func main() {
	// Initialize MongoDB connection
	initMongoDB()

	// Create a Gin router
	r := gin.Default()

	// Routes
	r.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "API de Logs funcionando correctamente.",
		})
	})

	r.POST("/logs", saveLog)
	r.GET("/logs", getAllLogs)              // Endpoint para obtener todos los logs
	r.GET("/logs/:email", getLogsByEmail)   // Endpoint para obtener logs de un usuario específico

	// Start the server
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080" // Default port
	}

	log.Printf("Servidor escuchando en el puerto %s", port)
	r.Run("0.0.0.0:8080")
}
