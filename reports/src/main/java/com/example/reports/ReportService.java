package com.example.reports;

import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class ReportService {

    private final ReportRepository repository;

    public ReportService(ReportRepository repository) {
        this.repository = repository;
    }

    // Obtener todos los reportes
    public List<ReportEntity> obtenerTodos() {
        return repository.findAll();
    }

    // Crear un nuevo reporte
    public ReportEntity crearReporte(ReportEntity reporte) {
        return repository.save(reporte);
    }

    // Obtener un reporte por ID
    public Optional<ReportEntity> obtenerPorId(Long id) {
        return repository.findById(id);
    }

    // Actualizar un reporte existente
    public ReportEntity actualizarReporte(Long id, ReportEntity reporteActualizado) {
        return repository.findById(id)
                .map(reporte -> {
                    reporte.setNombreInstitucion(reporteActualizado.getNombreInstitucion());
                    reporte.setNombreEstudiante(reporteActualizado.getNombreEstudiante());
                    reporte.setMensualidad(reporteActualizado.getMensualidad());
                    reporte.setDescuento(reporteActualizado.getDescuento());
                    reporte.setFechaUltimaPago(reporteActualizado.getFechaUltimaPago());
                    return repository.save(reporte);
                })
                .orElseThrow(() -> new RuntimeException("Reporte con ID " + id + " no encontrado."));
    }

    // Eliminar un reporte por ID
    public void eliminarReporte(Long id) {
        if (repository.existsById(id)) {
            repository.deleteById(id);
        } else {
            throw new RuntimeException("Reporte con ID " + id + " no encontrado.");
        }
    }
}
