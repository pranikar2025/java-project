package com.example.studybuddy1.service;

import com.example.studybuddy1.dto.CreateGroupRequest;
import com.example.studybuddy1.dto.GroupResponse;
import com.example.studybuddy1.entity.Membership;
import com.example.studybuddy1.entity.Student;
import com.example.studybuddy1.entity.StudyGroup;
import com.example.studybuddy1.entity.Subject;
import com.example.studybuddy1.repository.MembershipRepository;
import com.example.studybuddy1.repository.StudentRepository;
import com.example.studybuddy1.repository.StudyGroupRepository;
import com.example.studybuddy1.repository.SubjectRepository;
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
                .orElseThrow(() -> new RuntimeException("Subject not found with id: " + request.getSubjectId()));
        Student creator = studentRepository.findById(request.getCreatorId())
                .orElseThrow(() -> new RuntimeException("Student not found with id: " + request.getCreatorId()));

        StudyGroup group = new StudyGroup();
        group.setName(request.getName());
        group.setMaxMembers(request.getMaxMembers());
        group.setSubject(subject);
        group.setCreator(creator);

        group = groupRepository.save(group);

        // Auto-add creator as first member
        Membership m = new Membership();
        m.setStudyGroup(group);
        m.setStudent(creator);
        membershipRepository.save(m);

        return group;
    }

    public void joinGroup(Long groupId, Long studentId) {
        StudyGroup group = groupRepository.findById(groupId)
                .orElseThrow(() -> new RuntimeException("Group not found with id: " + groupId));
        Student student = studentRepository.findById(studentId)
                .orElseThrow(() -> new RuntimeException("Student not found with id: " + studentId));

        // Business Rule 1: Check group capacity
        int currentMembers = membershipRepository.countByStudyGroupId(groupId);
        if (currentMembers >= group.getMaxMembers()) {
            throw new RuntimeException("Group is full. Max members: " + group.getMaxMembers());
        }

        // Business Rule 2: Student cannot join same group twice
        if (membershipRepository.findByStudyGroupIdAndStudentId(groupId, studentId).isPresent()) {
            throw new RuntimeException("Student is already a member of this group");
        }

        Membership m = new Membership();
        m.setStudyGroup(group);
        m.setStudent(student);
        membershipRepository.save(m);
    }

    @Transactional
    public void leaveGroup(Long groupId, Long studentId) {
        if (!groupRepository.existsById(groupId)) {
            throw new RuntimeException("Group not found with id: " + groupId);
        }
        if (!studentRepository.existsById(studentId)) {
            throw new RuntimeException("Student not found with id: " + studentId);
        }
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
                .orElseThrow(() -> new RuntimeException("Group not found with id: " + groupId));

        // Only creator can remove members
        if (!group.getCreator().getId().equals(requesterId)) {
            throw new RuntimeException("Only the group creator can remove members");
        }

        membershipRepository.deleteByStudyGroupIdAndStudentId(groupId, studentToRemoveId);
    }
}
