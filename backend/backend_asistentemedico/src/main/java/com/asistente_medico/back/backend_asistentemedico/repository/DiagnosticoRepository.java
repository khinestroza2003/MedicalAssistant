package com.asistente_medico.back.backend_asistentemedico.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.asistente_medico.back.backend_asistentemedico.model.Diagnostico;

public interface DiagnosticoRepository extends JpaRepository<Diagnostico, Long> {
    
}
