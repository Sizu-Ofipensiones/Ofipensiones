package com.example.reports;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/reportes")
public class ReportController {

    private final ReportService service;

    public ReportController(ReportService service) {
        this.service = service;
    }

    // Obtener todos los reportes
    @GetMapping
    public List<ReportEntity> obtenerReportes() {
        return service.obtenerTodos();
    }

    // Crear un nuevo reporte
    @PostMapping
    public ReportEntity crearReporte(@RequestBody ReportEntity reporte) {
        return service.crearReporte(reporte);
    }

    // Obtener un reporte por ID
    @GetMapping("/{id}")
    public ResponseEntity<ReportEntity> obtenerPorId(@PathVariable Long id) {
        return service.obtenerPorId(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    // Actualizar un reporte existente por ID
    @PutMapping("/{id}")
    public ResponseEntity<ReportEntity> actualizarReporte(@PathVariable Long id, @RequestBody ReportEntity reporte) {
        try {
            return ResponseEntity.ok(service.actualizarReporte(id, reporte));
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }

    // Eliminar un reporte por ID
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminarReporte(@PathVariable Long id) {
        try {
            service.eliminarReporte(id);
            return ResponseEntity.noContent().build();
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }
}
