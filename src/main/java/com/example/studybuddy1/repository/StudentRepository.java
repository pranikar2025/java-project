package com.example.studybuddy1.repository;

import com.example.studybuddy1.entity.Student;
import org.springframework.data.jpa.repository.JpaRepository;

public interface StudentRepository extends JpaRepository<Student, Long> {
}
