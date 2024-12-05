package com.example.reports;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class ReportEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    private String nombreInstitucion;

    private String nombreEstudiante;

    private Float mensualidad;

    private Float descuento;

    private String fechaUltimaPago;

    // Getters y Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getNombreInstitucion() {
        return nombreInstitucion;
    }

    public void setNombreInstitucion(String nombreInstitucion) {
        this.nombreInstitucion = nombreInstitucion;
    }

    public String getNombreEstudiante() {
        return nombreEstudiante;
    }

    public void setNombreEstudiante(String nombreEstudiante) {
        this.nombreEstudiante = nombreEstudiante;
    }

    public Float getMensualidad() {
        return mensualidad;
    }

    public void setMensualidad(Float mensualidad) {
        this.mensualidad = mensualidad;
    }

    public Float getDescuento() {
        return descuento;
    }

    public void setDescuento(Float descuento) {
        this.descuento = descuento;
    }

    public String getFechaUltimaPago() {
        return fechaUltimaPago;
    }

    public void setFechaUltimaPago(String fechaUltimaPago) {
        this.fechaUltimaPago = fechaUltimaPago;
    }
}
