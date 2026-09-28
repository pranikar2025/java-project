package com.example.studybuddy1.repository;

import com.example.studybuddy1.entity.Membership;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface MembershipRepository extends JpaRepository<Membership, Long> {
    Optional<Membership> findByStudyGroupIdAndStudentId(Long studyGroupId, Long studentId);
    int countByStudyGroupId(Long studyGroupId);
    void deleteByStudyGroupIdAndStudentId(Long studyGroupId, Long studentId);
}
