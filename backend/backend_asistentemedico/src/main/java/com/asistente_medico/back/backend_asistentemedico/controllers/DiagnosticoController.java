package com.asistente_medico.back.backend_asistentemedico.controllers;

import org.springframework.web.bind.annotation.*;
import lombok.RequiredArgsConstructor;
import com.asistente_medico.back.backend_asistentemedico.services.DiagnosticoService;

import java.util.*;

@RestController
@RequestMapping("/api/diagnostico")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class DiagnosticoController {

    private final DiagnosticoService diagnosticoService;

    @PostMapping("/analizar")
    public List<String> obtenerDiagnosticos(@RequestBody Map<String, Object> datos) {
        String genero = (String) datos.get("genero");
        List<String> sintomas = (List<String>) datos.get("sintomas");
        int duracion = (int) datos.get("duracion_dias");

        return diagnosticoService.obtenerDiagnosticosProbables(genero, sintomas, duracion);
    }

    @GetMapping("/sintomas")
    public List<String> obtenerSintomas() {
       return diagnosticoService.obtenerTodosLosSintomas();
    }

}