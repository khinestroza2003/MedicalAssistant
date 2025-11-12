
package com.asistente_medico.back.backend_asistentemedico.model;

import jakarta.persistence.*;
import lombok.*;

import java.util.List;

@Entity
@Table(name = "diagnosticos")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Diagnostico {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id_diagnostico;

    @Column(nullable = false, length = 150, unique = true)
    private String nombre;

    @Column(columnDefinition = "TEXT")
    private String descripcion;

    // Relación inversa (opcional usarla si necesitas cargar desde diagnóstico los síntomas relacionados)
    @OneToMany(mappedBy = "diagnostico", cascade = CascadeType.ALL, fetch = FetchType.LAZY, orphanRemoval = true)
    private List<DiagnosticoSintoma> diagnosticoSintomas;
}