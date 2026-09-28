import os

base_dir = "f:/VS code/StudyBuddy1/src/main/java/com/example/StudyBuddy1"
os.makedirs(os.path.join(base_dir, "entity"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "repository"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "service"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "controller"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "exception"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "dto"), exist_ok=True)

static_dir = "f:/VS code/StudyBuddy1/src/main/resources/static"
os.makedirs(static_dir, exist_ok=True)

files = {
    f"{base_dir}/entity/Subject.java": """package com.example.StudyBuddy1.entity;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Data
public class Subject {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;
}
""",
    f"{base_dir}/entity/Student.java": """package com.example.StudyBuddy1.entity;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Data
public class Student {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;
    private String email;
}
""",
    f"{base_dir}/entity/StudyGroup.java": """package com.example.StudyBuddy1.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.util.List;

@Entity
@Data
public class StudyGroup {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;
    private int maxMembers;

    @ManyToOne
    @JoinColumn(name = "subject_id")
    private Subject subject;

    @ManyToOne
    @JoinColumn(name = "creator_id")
    private Student creator;

    @OneToMany(mappedBy = "studyGroup")
    private List<Membership> memberships;
}
""",
    f"{base_dir}/entity/Membership.java": """package com.example.StudyBuddy1.entity;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Data
public class Membership {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "student_id")
    private Student student;

    @ManyToOne
    @JoinColumn(name = "study_group_id")
    private StudyGroup studyGroup;
}
""",
    f"{base_dir}/repository/SubjectRepository.java": """package com.example.StudyBuddy1.repository;

import com.example.StudyBuddy1.entity.Subject;
import org.springframework.data.jpa.repository.JpaRepository;

public interface SubjectRepository extends JpaRepository<Subject, Long> {}
""",
    f"{base_dir}/repository/StudentRepository.java": """package com.example.StudyBuddy1.repository;

import com.example.StudyBuddy1.entity.Student;
import org.springframework.data.jpa.repository.JpaRepository;

public interface StudentRepository extends JpaRepository<Student, Long> {}
""",
    f"{base_dir}/repository/StudyGroupRepository.java": """package com.example.StudyBuddy1.repository;

import com.example.StudyBuddy1.entity.StudyGroup;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface StudyGroupRepository extends JpaRepository<StudyGroup, Long> {
    List<StudyGroup> findBySubjectId(Long subjectId);
}
""",
    f"{base_dir}/repository/MembershipRepository.java": """package com.example.StudyBuddy1.repository;

import com.example.StudyBuddy1.entity.Membership;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface MembershipRepository extends JpaRepository<Membership, Long> {
    Optional<Membership> findByStudyGroupIdAndStudentId(Long studyGroupId, Long studentId);
    int countByStudyGroupId(Long studyGroupId);
    void deleteByStudyGroupIdAndStudentId(Long studyGroupId, Long studentId);
}
""",
    f"{base_dir}/exception/GlobalExceptionHandler.java": """package com.example.StudyBuddy1.exception;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<String> handleRuntimeException(RuntimeException e) {
        return ResponseEntity.badRequest().body(e.getMessage());
    }
}
""",
    f"{base_dir}/dto/CreateGroupRequest.java": """package com.example.StudyBuddy1.dto;

import lombok.Data;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

@Data
public class CreateGroupRequest {
    @NotBlank
    private String name;
    @Positive
    private int maxMembers;
    @NotNull
    private Long subjectId;
    @NotNull
    private Long creatorId;
}
""",
    f"{base_dir}/dto/GroupResponse.java": """package com.example.StudyBuddy1.dto;
import lombok.Data;

@Data
public class GroupResponse {
    private Long id;
    private String name;
    private int maxMembers;
    private int currentMembers;
}
""",
    f"{base_dir}/service/StudyBuddyService.java": """package com.example.StudyBuddy1.service;

import com.example.StudyBuddy1.dto.CreateGroupRequest;
import com.example.StudyBuddy1.dto.GroupResponse;
import com.example.StudyBuddy1.entity.Membership;
import com.example.StudyBuddy1.entity.Student;
import com.example.StudyBuddy1.entity.StudyGroup;
import com.example.StudyBuddy1.entity.Subject;
import com.example.StudyBuddy1.repository.MembershipRepository;
import com.example.StudyBuddy1.repository.StudentRepository;
import com.example.StudyBuddy1.repository.StudyGroupRepository;
import com.example.StudyBuddy1.repository.SubjectRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class StudyBuddyService {
    @Autowired
    private StudyGroupRepository groupRepository;
    @Autowired
    private MembershipRepository membershipRepository;
    @Autowired
    private StudentRepository studentRepository;
    @Autowired
    private SubjectRepository subjectRepository;

    public StudyGroup createGroup(CreateGroupRequest request) {
        Subject subject = subjectRepository.findById(request.getSubjectId())
                .orElseThrow(() -> new RuntimeException("Subject not found"));
        Student creator = studentRepository.findById(request.getCreatorId())
                .orElseThrow(() -> new RuntimeException("Creator not found"));

        StudyGroup group = new StudyGroup();
        group.setName(request.getName());
        group.setMaxMembers(request.getMaxMembers());
        group.setSubject(subject);
        group.setCreator(creator);

        group = groupRepository.save(group);

        // Add creator as member
        Membership m = new Membership();
        m.setStudyGroup(group);
        m.setStudent(creator);
        membershipRepository.save(m);

        return group;
    }

    public void joinGroup(Long groupId, Long studentId) {
        StudyGroup group = groupRepository.findById(groupId)
                .orElseThrow(() -> new RuntimeException("Group not found"));
        Student student = studentRepository.findById(studentId)
                .orElseThrow(() -> new RuntimeException("Student not found"));

        int currentMembers = membershipRepository.countByStudyGroupId(groupId);
        if (currentMembers >= group.getMaxMembers()) {
            throw new RuntimeException("Group is full");
        }

        if (membershipRepository.findByStudyGroupIdAndStudentId(groupId, studentId).isPresent()) {
            throw new RuntimeException("Student already in group");
        }

        Membership m = new Membership();
        m.setStudyGroup(group);
        m.setStudent(student);
        membershipRepository.save(m);
    }

    @Transactional
    public void leaveGroup(Long groupId, Long studentId) {
        membershipRepository.deleteByStudyGroupIdAndStudentId(groupId, studentId);
    }

    public List<GroupResponse> listGroupsBySubject(Long subjectId) {
        return groupRepository.findBySubjectId(subjectId).stream().map(group -> {
            GroupResponse res = new GroupResponse();
            res.setId(group.getId());
            res.setName(group.getName());
            res.setMaxMembers(group.getMaxMembers());
            res.setCurrentMembers(membershipRepository.countByStudyGroupId(group.getId()));
            return res;
        }).collect(Collectors.toList());
    }

    @Transactional
    public void removeMember(Long groupId, Long requesterId, Long studentToRemoveId) {
        StudyGroup group = groupRepository.findById(groupId)
                .orElseThrow(() -> new RuntimeException("Group not found"));
        if (!group.getCreator().getId().equals(requesterId)) {
            throw new RuntimeException("Only group creator can remove members");
        }
        membershipRepository.deleteByStudyGroupIdAndStudentId(groupId, studentToRemoveId);
    }
}
""",
    f"{base_dir}/controller/StudyBuddyController.java": """package com.example.StudyBuddy1.controller;

import com.example.StudyBuddy1.dto.CreateGroupRequest;
import com.example.StudyBuddy1.dto.GroupResponse;
import com.example.StudyBuddy1.entity.Student;
import com.example.StudyBuddy1.entity.StudyGroup;
import com.example.StudyBuddy1.entity.Subject;
import com.example.StudyBuddy1.repository.StudentRepository;
import com.example.StudyBuddy1.repository.SubjectRepository;
import com.example.StudyBuddy1.service.StudyBuddyService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import jakarta.validation.Valid;

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
        return ResponseEntity.ok("Left successfully");
    }

    @GetMapping("/subjects/{subjectId}/groups")
    public ResponseEntity<List<GroupResponse>> listGroups(@PathVariable Long subjectId) {
        return ResponseEntity.ok(service.listGroupsBySubject(subjectId));
    }

    @DeleteMapping("/groups/{groupId}/members/{studentId}")
    public ResponseEntity<String> removeMember(@PathVariable Long groupId, @PathVariable Long studentId, @RequestParam Long requesterId) {
        service.removeMember(groupId, requesterId, studentId);
        return ResponseEntity.ok("Member removed successfully");
    }

    @GetMapping("/students")
    public ResponseEntity<List<Student>> getStudents() {
        return ResponseEntity.ok(studentRepository.findAll());
    }
    
    @PostMapping("/students")
    public ResponseEntity<Student> createStudent(@RequestBody Student student) {
        return ResponseEntity.ok(studentRepository.save(student));
    }

    @GetMapping("/subjects")
    public ResponseEntity<List<Subject>> getSubjects() {
        return ResponseEntity.ok(subjectRepository.findAll());
    }

    @PostMapping("/subjects")
    public ResponseEntity<Subject> createSubject(@RequestBody Subject subject) {
        return ResponseEntity.ok(subjectRepository.save(subject));
    }
}
""",
    f"{static_dir}/index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StudyBuddy - Group Formation Tool</title>
    <style>
        :root {
            --primary: #4F46E5;
            --primary-dark: #4338CA;
            --secondary: #10B981;
            --danger: #EF4444;
            --dark: #1F2937;
            --light: #F3F4F6;
            --white: #FFFFFF;
        }
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--light);
            color: var(--dark);
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .card {
            background: var(--white);
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        input, select, button {
            padding: 10px;
            margin: 5px 0;
            border: 1px solid #D1D5DB;
            border-radius: 4px;
            width: 100%;
            box-sizing: border-box;
        }
        button {
            background-color: var(--primary);
            color: white;
            border: none;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.3s;
        }
        button:hover {
            background-color: var(--primary-dark);
        }
        .btn-danger {
            background-color: var(--danger);
        }
        .btn-success {
            background-color: var(--secondary);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #E5E7EB;
        }
        th {
            background-color: #F9FAFB;
        }
        .flex {
            display: flex;
            gap: 10px;
        }
        .flex-1 {
            flex: 1;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 StudyBuddy</h1>
            <p>Student Study Group Formation Tool</p>
        </div>

        <div class="flex">
            <!-- Setup Dummy Data -->
            <div class="card flex-1">
                <h3>1. Quick Setup (Admin)</h3>
                <p>Create mock subjects and students to test the app.</p>
                <div class="flex">
                    <input type="text" id="subjectName" placeholder="Subject Name (e.g. Math)">
                    <button onclick="createSubject()">Add Subject</button>
                </div>
                <div class="flex" style="margin-top: 10px;">
                    <input type="text" id="studentName" placeholder="Student Name">
                    <button onclick="createStudent()">Add Student</button>
                </div>
            </div>

            <!-- Create Group -->
            <div class="card flex-1">
                <h3>2. Create a Study Group</h3>
                <input type="text" id="groupName" placeholder="Group Name">
                <input type="number" id="maxMembers" placeholder="Max Members" min="1">
                <select id="groupSubject"></select>
                <select id="groupCreator"></select>
                <button class="btn-success" onclick="createGroup()">Create Group</button>
            </div>
        </div>

        <!-- Groups List -->
        <div class="card">
            <h3>3. View & Join Groups</h3>
            <div class="flex">
                <select id="filterSubject" class="flex-1"></select>
                <button onclick="loadGroups()" style="width: auto; padding: 10px 20px;">Load Groups</button>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Members</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="groupsTable">
                    <!-- Data here -->
                </tbody>
            </table>
        </div>
        
        <!-- Simulate User Action -->
        <div class="card">
            <h3>Current User Actions (Simulated)</h3>
            <select id="currentUser"></select>
            <p>Select a student above, then use the Join/Leave buttons in the table to act as them.</p>
        </div>

    </div>

    <script>
        const API_URL = 'http://localhost:8080/api';

        async function init() {
            await loadSubjects();
            await loadStudents();
        }

        async function createSubject() {
            const name = document.getElementById('subjectName').value;
            if(!name) return;
            await fetch(`${API_URL}/subjects`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name})
            });
            document.getElementById('subjectName').value = '';
            loadSubjects();
        }

        async function createStudent() {
            const name = document.getElementById('studentName').value;
            if(!name) return;
            await fetch(`${API_URL}/students`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name, email: name.toLowerCase()+'@example.com'})
            });
            document.getElementById('studentName').value = '';
            loadStudents();
        }

        async function loadSubjects() {
            const res = await fetch(`${API_URL}/subjects`);
            const data = await res.json();
            const options = data.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
            document.getElementById('groupSubject').innerHTML = options;
            document.getElementById('filterSubject').innerHTML = options;
        }

        async function loadStudents() {
            const res = await fetch(`${API_URL}/students`);
            const data = await res.json();
            const options = data.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
            document.getElementById('groupCreator').innerHTML = options;
            document.getElementById('currentUser').innerHTML = options;
        }

        async function createGroup() {
            const payload = {
                name: document.getElementById('groupName').value,
                maxMembers: document.getElementById('maxMembers').value,
                subjectId: document.getElementById('groupSubject').value,
                creatorId: document.getElementById('groupCreator').value
            };
            const res = await fetch(`${API_URL}/groups`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });
            if(res.ok) {
                alert('Group created!');
                loadGroups();
            } else {
                alert(await res.text());
            }
        }

        async function loadGroups() {
            const subjectId = document.getElementById('filterSubject').value;
            if(!subjectId) return;
            const res = await fetch(`${API_URL}/subjects/${subjectId}/groups`);
            const groups = await res.json();
            
            document.getElementById('groupsTable').innerHTML = groups.map(g => `
                <tr>
                    <td>${g.id}</td>
                    <td>${g.name}</td>
                    <td>${g.currentMembers} / ${g.maxMembers}</td>
                    <td>
                        <button onclick="joinGroup(${g.id})" style="width: auto;">Join</button>
                        <button class="btn-danger" onclick="leaveGroup(${g.id})" style="width: auto;">Leave</button>
                    </td>
                </tr>
            `).join('');
        }

        async function joinGroup(groupId) {
            const studentId = document.getElementById('currentUser').value;
            const res = await fetch(`${API_URL}/groups/${groupId}/join?studentId=${studentId}`, {method: 'POST'});
            if(res.ok) alert('Joined successfully'); else alert(await res.text());
            loadGroups();
        }

        async function leaveGroup(groupId) {
            const studentId = document.getElementById('currentUser').value;
            const res = await fetch(`${API_URL}/groups/${groupId}/leave?studentId=${studentId}`, {method: 'POST'});
            if(res.ok) alert('Left successfully'); else alert(await res.text());
            loadGroups();
        }

        window.onload = init;
    </script>
</body>
</html>
"""
}

for filepath, content in files.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Files created successfully.")
