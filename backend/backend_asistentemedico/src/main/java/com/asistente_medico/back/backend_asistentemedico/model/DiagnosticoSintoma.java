package com.asistente_medico.back.backend_asistentemedico.model;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "diagnostico_sintomas")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor

public class DiagnosticoSintoma {
    

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_diagnostico", nullable = false)
    private Diagnostico diagnostico;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id_sintoma", nullable = false)
    private Sintoma sintoma;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Genero genero = Genero.Ambos;

    @Column(name = "duracion_min_dias", nullable = false)
    private int duracion_min_dias = 0;

    @Column(name = "duracion_max_dias", nullable = false)
    private int duracion_max_dias = 365; // valor grande por defecto

}
