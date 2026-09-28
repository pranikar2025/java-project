package com.example.studybuddy1.controller;

import com.example.studybuddy1.dto.CreateGroupRequest;
import com.example.studybuddy1.dto.GroupResponse;
import com.example.studybuddy1.entity.Student;
import com.example.studybuddy1.entity.StudyGroup;
import com.example.studybuddy1.entity.Subject;
import com.example.studybuddy1.repository.StudentRepository;
import com.example.studybuddy1.repository.SubjectRepository;
import com.example.studybuddy1.service.StudyBuddyService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api")
@CrossOrigin("*")
public class StudyBuddyController {

    @Autowired
    private StudyBuddyService service;

    @Autowired
    private StudentRepository studentRepository;

    @Autowired
    private SubjectRepository subjectRepository;

    // ===== GROUP ENDPOINTS =====

    @PostMapping("/groups")
    public ResponseEntity<StudyGroup> createGroup(@Valid @RequestBody CreateGroupRequest request) {
        return ResponseEntity.ok(service.createGroup(request));
    }

    @PostMapping("/groups/{groupId}/join")
    public ResponseEntity<String> joinGroup(@PathVariable Long groupId, @RequestParam Long studentId) {
        service.joinGroup(groupId, studentId);
        return ResponseEntity.ok("Joined successfully");
    }

    @PostMapping("/groups/{groupId}/leave")
    public ResponseEntity<String> leaveGroup(@PathVariable Long groupId, @RequestParam Long studentId) {
        service.leaveGroup(groupId, studentId);
        return ResponseEntity.ok("Left group successfully");
    }

    @GetMapping("/subjects/{subjectId}/groups")
    public ResponseEntity<List<GroupResponse>> listGroups(@PathVariable Long subjectId) {
        return ResponseEntity.ok(service.listGroupsBySubject(subjectId));
    }

    @DeleteMapping("/groups/{groupId}/members/{studentId}")
    public ResponseEntity<String> removeMember(
            @PathVariable Long groupId,
            @PathVariable Long studentId,
            @RequestParam Long requesterId) {
        service.removeMember(groupId, requesterId, studentId);
        return ResponseEntity.ok("Member removed successfully");
    }

    // ===== STUDENT ENDPOINTS =====

    @GetMapping("/students")
    public ResponseEntity<List<Student>> getStudents() {
        return ResponseEntity.ok(studentRepository.findAll());
    }

    @PostMapping("/students")
    public ResponseEntity<Student> createStudent(@RequestBody Student student) {
        return ResponseEntity.ok(studentRepository.save(student));
    }

    // ===== SUBJECT ENDPOINTS =====

    @GetMapping("/subjects")
    public ResponseEntity<List<Subject>> getSubjects() {
        return ResponseEntity.ok(subjectRepository.findAll());
    }

    @PostMapping("/subjects")
    public ResponseEntity<Subject> createSubject(@RequestBody Subject subject) {
        return ResponseEntity.ok(subjectRepository.save(subject));
    }
}
