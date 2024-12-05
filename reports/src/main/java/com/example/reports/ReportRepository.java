package com.example.reports;

import org.springframework.stereotype.Repository;
import org.springframework.data.jpa.repository.JpaRepository;

@Repository
public interface ReportRepository extends JpaRepository<ReportEntity, Long> {

}
