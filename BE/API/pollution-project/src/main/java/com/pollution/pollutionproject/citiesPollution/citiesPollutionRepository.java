package com.pollution.pollutionproject.citiesPollution;

import com.pollution.pollutionproject.citiescoordinate.citiesCoordinate;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDate;
import java.util.Collection;

public interface citiesPollutionRepository extends JpaRepository<citiesPollution, Integer> {

    @Query(value = "SELECT * FROM CITIES_POLLUTION c WHERE c.CITY_ID = :id and c.date >= :fromDate and c.date <= :toDate ",
            nativeQuery = true)
    Collection<citiesPollution> historicalDataPerCity(@Param("id") int id,
                                                      @Param("fromDate") LocalDate fromDate,
                                                      @Param("toDate") LocalDate toDate);


    @Query(value = "SELECT * FROM CITIES_POLLUTION c WHERE c.CITY_ID = ?1 and c.date >= ?2 and c.date <= ?3 ",
            nativeQuery = true)
    Collection<citiesPollution> historicalDataPerCityv2( int id, LocalDate fromDate,LocalDate toDate);

    @Query(value = "SELECT * FROM CITIES_POLLUTION c WHERE c.CITY_ID = :id order by c.DATE desc ",
            nativeQuery = true)
    Collection<citiesPollution> historicalAllDataPerCity(@Param("id") int id);

    @Query(value = "SELECT * FROM CITIES_POLLUTION c order by c.DATE desc ",
            nativeQuery = true)
    Collection<citiesPollution> historicalAllDataAllCities();
}
