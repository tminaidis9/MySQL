#1

SELECT p.SSN, p.Name, count(*) AS TotalStay , SUM(tr.cost) AS TotalCost
FROM undergoes un, stay s,treatment tr, patient p
WHERE( un.Patient = p.SSN  AND s.StayID = un.Stay AND s.StayStart = un.DateUndergoes AND tr.Code = un.Treatment AND p.Age <= 40 AND p.Age >= 30 AND p.Gender = 'male')
GROUP BY p.SSN
HAVING count(*) > 1

#2
SELECT n.EmployeeID, n.Name
FROM nurse n
WHERE n.EmployeeID in
	(
		SELECT onc.Nurse
        FROM on_call onc
        WHERE ( onc.Nurse = n.EmployeeID AND (onc.BlockFloor >=4 AND onc.BlockFloor <= 7) AND onc.OnCallStart >= '2008-04-20 23:22:00' AND onc.OnCallEnd <= '2009-06-04 11:00:00')
        GROUP BY onc.Nurse
        HAVING count( DISTINCT onc.BlockCode) > 1
    )
GROUP BY n.EmployeeID, n.Name

#3

SELECT p.SSN, p.Name
FROM patient p
WHERE ( p.Gender = 'female' AND p.Age > 40 AND EXISTS
		(
			SELECT v.patient_SSN, num_of_doses
            FROM vaccination v, vaccines va
            WHERE( v.patient_SSN = p.SSN AND va.vax_name = v.vaccines_vax_name)
            GROUP BY v.patient_SSN, va.num_of_doses
            HAVING count(*) = va.num_of_doses
        )
	  )
GROUP BY p.SSN, p.Name

#4

SELECT m.Name, m.Brand, count( DISTINCT p.patient) AS PATIENTS
FROM medication m, prescribes p
WHERE (p.Medication = m.Code)
GROUP BY m.code, m.Name, m.Brand
HAVING count( DISTINCT p.patient) > 1

#5
SELECT p.SSN
FROM patient p
WHERE 1 = 
	(
	 SELECT count( DISTINCT v.physician_EmployeeID)
     FROM vaccination v, vaccines va
     WHERE v.patient_SSN = p.SSN AND va.vax_name = v.vaccines_vax_name
    )

#6

SELECT 'yes' AS answer
FROM stay s
WHERE s.Room NOT IN
	(
     SELECT s1.Room
	 FROM stay s1
     WHERE ( s1.StayStart <= '2013-12-31 23:59:59' AND s1.StayEnd >= '2013-01-01 00:00:00')
	)    
GROUP BY s.Room
HAVING count(*) > 0

UNION

SELECT 'no' AS answer
FROM stay s
WHERE s.Room NOT IN
	(
     SELECT s1.Room
	 FROM stay s1
     WHERE ( s1.StayStart <= '2013-12-31 23:59:59' AND s1.StayEnd >= '2013-01-01 00:00:00')
	)    
GROUP BY s.Room
HAVING count(*) = 0

#7

SELECT ph.EmployeeID, ph.Name, count( DISTINCT u.Patient) AS Patient
FROM physician ph, undergoes u
WHERE( ph.Position = 'PATHOLOGY' AND ph.EmployeeID = u.Physician)
GROUP BY ph.EmployeeID
UNION
SELECT ph.EmployeeID, ph.Name, '0' AS Patient
FROM physician ph
WHERE( ph.Position = 'PATHOLOGY' AND 0=
		(
         SELECT count( DISTINCT u.Patient)
         FROM undergoes u
         WHERE ph.EmployeeID = u.Physician
		)
    )
GROUP BY ph.EmployeeID

#8
SELECT p.Name
FROM patient p
WHERE( EXISTS
		(
			SELECT v.patient_SSN, va.num_of_doses
            FROM vaccination v, vaccines va
			WHERE( v.vaccines_vax_name = va.vax_name AND p.SSN = v.patient_SSN)
            GROUP BY v.patient_SSN, va.num_of_doses
            HAVING count(*) < 2
        )
        OR p.SSN <> ALL
        (
			SELECT v.patient_SSN
            FROM vaccination v
			GROUP BY v.patient_SSN
        )
        
	 )
     
#9

SELECT va.vax_name
FROM vaccines va, vaccination v1
WHERE( va.vax_name  = v1.vaccines_vax_name)
GROUP BY va.vax_name
HAVING count(*) >= ALL		
        (
			SELECT count(*)
            FROM vaccination v
			GROUP BY v.vaccines_vax_name
        )
        
#10

SELECT ph.Name
FROM physician ph, trained_in tr_i, treatment tr
WHERE( ph.EmployeeID = tr_i.Physician AND tr.Code = tr_i.Speciality AND tr.Name = 'RADIATION ONCOLOGY')
GROUP BY ph.EmployeeID
HAVING count(*) = 
	(
		SELECT count(*)
        FROM treatment tr1
        WHERE tr1.Name = 'RADIATION ONCOLOGY'
    )