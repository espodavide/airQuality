package com.pollution.pollutionproject.citiescoordinate;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.Collection;

@Repository
public interface citiesCoordinateRepository extends JpaRepository<citiesCoordinate, Integer> {
    @Query(
            value = "SELECT * FROM cities c WHERE c.name like '%Bergamo%' ",
            nativeQuery = true)
    Collection<citiesCoordinate> findBergamo();

}
