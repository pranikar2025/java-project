package com.example.studybuddy1.repository;

import com.example.studybuddy1.entity.Subject;
import org.springframework.data.jpa.repository.JpaRepository;

public interface SubjectRepository extends JpaRepository<Subject, Long> {
}
