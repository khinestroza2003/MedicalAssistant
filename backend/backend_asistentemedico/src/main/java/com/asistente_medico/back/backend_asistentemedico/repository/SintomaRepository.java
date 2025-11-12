package com.asistente_medico.back.backend_asistentemedico.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.asistente_medico.back.backend_asistentemedico.model.Sintoma;

public interface SintomaRepository extends JpaRepository<Sintoma, Long> {
    Sintoma findByNombreIgnoreCase(String nombre);
}
