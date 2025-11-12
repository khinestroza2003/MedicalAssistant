package com.asistente_medico.back.backend_asistentemedico.services;

import org.springframework.stereotype.Service;
import lombok.RequiredArgsConstructor;
import com.asistente_medico.back.backend_asistentemedico.repository.*;
import com.asistente_medico.back.backend_asistentemedico.model.*;

import java.util.*;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class DiagnosticoService {

    private final DiagnosticoSintomaRepository diagnosticoSintomaRepository;
    private final SintomaRepository sintomaRepository;

    public List<String> obtenerDiagnosticosProbables(String genero, List<String> sintomasIngresados, int duracionDias) {
        Genero generoEnum = Genero.valueOf(genero);

        // Buscar síntomas que coincidan con los nombres ingresados
        List<Sintoma> sintomas = sintomasIngresados.stream()
                .map(nombre -> sintomaRepository.findByNombreIgnoreCase(nombre))
                .filter(Objects::nonNull)
                .collect(Collectors.toList());

        if (sintomas.isEmpty()) return List.of("No se encontraron síntomas válidos.");

        // Buscar diagnósticos que contengan esos síntomas y coincidan en género y duración
        List<DiagnosticoSintoma> relaciones = diagnosticoSintomaRepository.findByGeneroOrGenero(generoEnum, Genero.Ambos);

        Map<Diagnostico, Long> coincidencias = relaciones.stream()
                .filter(rel -> sintomas.contains(rel.getSintoma()))
                .filter(rel -> duracionDias >= rel.getDuracion_min_dias() && duracionDias <= rel.getDuracion_max_dias())
                .collect(Collectors.groupingBy(DiagnosticoSintoma::getDiagnostico, Collectors.counting()));

        return coincidencias.entrySet().stream()
                .sorted(Map.Entry.<Diagnostico, Long>comparingByValue().reversed())
                .map(e -> e.getKey().getNombre())
                .collect(Collectors.toList());
    }

        public List<String> obtenerTodosLosSintomas() {
                return sintomaRepository.findAll().stream()
                        .map(Sintoma::getNombre)
                        .collect(Collectors.toList());
        }
}