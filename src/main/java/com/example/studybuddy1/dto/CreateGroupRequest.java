package com.example.studybuddy1.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

public class CreateGroupRequest {

    @NotBlank
    private String name;

    @Positive
    private int maxMembers;

    @NotNull
    private Long subjectId;

    @NotNull
    private Long creatorId;

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public int getMaxMembers() { return maxMembers; }
    public void setMaxMembers(int maxMembers) { this.maxMembers = maxMembers; }

    public Long getSubjectId() { return subjectId; }
    public void setSubjectId(Long subjectId) { this.subjectId = subjectId; }

    public Long getCreatorId() { return creatorId; }
    public void setCreatorId(Long creatorId) { this.creatorId = creatorId; }
}
