package com.example.studybuddy1.repository;

import com.example.studybuddy1.entity.StudyGroup;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface StudyGroupRepository extends JpaRepository<StudyGroup, Long> {
    List<StudyGroup> findBySubjectId(Long subjectId);
}
