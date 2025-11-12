
package com.asistente_medico.back.backend_asistentemedico.model;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "sintomas")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class Sintoma {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @EqualsAndHashCode.Include
    private Long id_sintoma;

    @Column(nullable = false, length = 150, unique = true)
    private String nombre;

    @Column(columnDefinition = "TEXT")
    private String descripcion;
}