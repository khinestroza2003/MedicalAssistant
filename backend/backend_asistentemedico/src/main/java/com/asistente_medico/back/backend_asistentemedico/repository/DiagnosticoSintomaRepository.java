package com.asistente_medico.back.backend_asistentemedico.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.asistente_medico.back.backend_asistentemedico.model.*;
import java.util.List;

public interface DiagnosticoSintomaRepository extends JpaRepository<DiagnosticoSintoma, Long> {

    List<DiagnosticoSintoma> findByGeneroOrGenero(Genero genero, Genero ambos);
    
}