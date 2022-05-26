#sdi1900113 theodoros minaidis
# logw problimatwn me thn efarmogi ths mySQL ( den kataferame oute me thn boitheia tou upeuthinou tou ergasthriou na bgaloume kapoia akri ) ola eginan xwris tis aparaithtes dokimes me to arxeio pou dwthike kati pou shmainei oti xwris tous elegxous autous tha uparxoun polla lathoi pou den mporesa na entopisw
# prospathisa mexri teleutaia mera shmera na to diorthwsw den ta katafera kai den exw dystyxws allo pc gia na asxolithw me thn ergasia.
# elpizw an einai dunaton na bathmologitheitai me basi kai thn prospatheia kai oxi mono to apotelesma. to am mou einai sdi1900113 eixame 
# epikoinwnisei kai me ton k.kuriakako ama thelete na to eksakribwsete.

#1
 
select SUM(treatment.cost) AS Payement
from treatment, patient,undergoes
where patient.Gender = "male" AND patient.Age >= 30 AND patient.Age <= 40 AND patient.SSN = undergoes.Patient and undergoes.Treatment = treatment.Code                                
group by patient.Name
having COUNT(*)>1;

#2

select distinct n
from on_call nc, nurse n
where oc.Nurse = n.EmployeeID AND (oc.BlockFloor >= 4 AND oc.BlockFloor >= 7) AND (oc.OnCallStart>='2008-04-20 23:22:00' AND oc.OnCallEnd<='2009-06-04 11:00:00') AND EXISTS(select * from on_call oc2 where oc2.Nurse = n.EmployeeID AND (oc2.BlockFloor >= 4 AND oc2.BlockFloor >= 7) AND (oc2.OnCallStart>='2008-04-20 23:22:00' AND oc2.OnCallEnd<='2009-06-04 11:00:00') AND oc2.OnCallStart<>oc.OnCallStart AND oc2.OnCallEnd<>oc2.OnCallEnd );

#3

select distinct p
from patient, vaccination , vaccines
where patient.Gender = "female" AND patient.SSN = vaccination.patient AND patient.Age > 40 AND vaccines.vax_name = vaccination.vax_name AND vaccines.num_of_doses = ANY (select COUNT(*) from vaccinatiom v2 where v2.patient = patient.SSN);

#4

select m.Name, m.Brand, COUNT(distinct p.SSN)
from emdication m, patient p, prescribes pr
where pr.patient IN (select pr2.patient from prescribes pr2 where pr2.Medication = pr.Medication group by pr2.patient having COUNT(*) >= 2) AND pr.Medication =  m.Code AND p.SSN = pr.patient ;

#5

select distinct p.SSN from patient p, vaccination v, vaccines vs
where vs.num_of_doses = ANY (select COUNT(*) from vaccination v2 where (v2.patient = v.patient AND  v.nurse = v2.nurse));

#6

Select 'yes' AS answer
Where not exists(select * from stay,room where stay.Room = room.RoomNumber AND stay.StayEnd >= '2013-01-01 00:00:00' AND stay.StayStart <= '2013-12-31 23:59:59')
UNION
Select 'no' AS answer
Where exists(select * from stay,room where stay.Room = room.RoomNumber AND stay.StayEnd >= '2013-01-01 00:00:00' AND stay.StayStart <= '2013-12-31 23:59:59')
;
#7

select distinct ph.EmployeeID, ph.Name, COUNT(distinct p.SSN) from physician ph, patient p
where 1 = ANY(select COUNT(*) from trained_in where trained_in.physician = ph.EmployeeID AND trained_in.speciality = "PATHOLOGY" ) AND 1 >= ANY (select COUNT(*) from undergoes where undergoes.Patient = p.SSN AND undergoes.Physician = ph.EmployeeID) 
;
#8

select distinct p.Name from patient p, vaccination v, vaccines vs where vs.vax_name = v.vax_name AND v.patient = p.SSN group by p.Name having COUNT(*) = vs.num_of_doses
UNION
select distinct p.Name from patient p, vaccination v, vaccines vs where vs.vax_name = v.vax_name AND NOT EXISTS (select * from patient p2, vaccination v2 where patient.SSN = vaccination_patient_SSN)
;
#9


#10