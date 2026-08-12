# asep

Extract data from Greek ASEP for education

INFO: πινακεσ αναπληρωτων προσληψεις site:www.minedu.gov.gr

## Actions

### TODO

- Import/Update all data

### Review

- Say who has penalty or not
- Say who has permanent place or not
- Say order in list based on

## SQL Queries

### Give me all order by total_score

```sql
SELECT e.*, q.* 
FROM educator as e 
INNER JOIN qualifications as q 
WHERE 
    e.am = q.am 
ORDER BY q.total_score DESC
```

```sql
SELECT e.*, q.* 
FROM educator as e 
INNER JOIN qualifications as q 
WHERE 
    e.am = q.am AND
    e.am = "68753"
ORDER BY q.total_score DESC;
```

```sql
SELECT e.*, q.*
FROM educator AS e INNER JOIN qualifications AS q ON e.am = q.am
WHERE e.lastname LIKE '%ΚΑΝΑΚΗΣ%' AND e.name LIKE 'ΙΩΑ%' AND e.father LIKE 'ΣΤΑ%' AND q.spec LIKE 'ΠΕ02%'
```

### Double Rows

```sql
SELECT e.*, count(*)
FROM educator as e 
GROUP BY e.adt
HAVING count(*) >1;
```

### Teachers with multi positions

```sql
SELECT e.*, count(*)
FROM educator as e 
INNER JOIN qualifications as q 
WHERE 
    e.id = q.educator_id
GROUP BY e.adt
HAVING count(*) > 1;
```

```sql
select ee.*, qq.* 
from educator as ee 
inner join qualifications as qq
where ee.id in (
    SELECT e.id
    FROM educator as e
    INNER JOIN qualifications as q
    WHERE e.id = q.educator_id
    GROUP BY e.adt
    HAVING count(*) > 1
) 
AND ee.id = qq.educator_id
Order By ee.adt;
```


## Anaplirotes

### Year 2021-22

- [???]()

### Year 2022-23

- [???]()

### Year 2023-24

- [A Round / ???]()
- [B Round / 25-10-23](https://www.minedu.gov.gr/news/56912-25-10-23-proslipseis-2-763-ekpaideftikon-protovathmias-kai-defterovathmias-ekpaidefsis-sti-geniki-ekpaidefsi-os-prosorinon-anapliroton-me-sxesi-ergasias-idiotikoy-dikaiou-orismenou-xronou-gia-to-didaktiko-etos-2023-2024)
- [C Round / 28-11-23](https://www.minedu.gov.gr/ypapegan/anakoinoseis/57168-28-11-23-proslipseis-4-593-ekpaideftikon-protovathmias-kai-defterovathmias-ekpaidefsis-stin-eidiki-agogi-kai-ekpaidefsi-kai-stin-geniki-ekpaidefsi-os-prosorinon-anapliroton-me-sxesi-ergasias-idiotikoy-dikaiou-orismenou-xronou-gia-to-didaktiko-etos-2023-2025)
- [D Round / 28-12-23](https://www.minedu.gov.gr/news/57423-28-12-23-proslipseis-521-ekpaideftikon-avathmias-kai-vvathmias-ekpaidefsis-stin-eidiki-agogi-kai-ekpaidefsi-kathos-kai-sti-geniki-ekpaidefsi-os-prosorinon-anapliroton-me-sxesi-ergasias-idiotikoy-dikaiou-orismenou-xronou-gia-to-sx-etos-2023-2024)
- [E Round / 21-02-24](https://www.minedu.gov.gr/news/57743-21-02-24-289)
- [F Round / 14-03-24](https://www.minedu.gov.gr/news/57891-14-03-24-130-2023-2024)
- [G Round / 16-04-24](https://www.minedu.gov.gr/news/58136-16-04-24-106-2023-2024)

## Nomimopoihsh

### 2024

- [21-08-24](https://www.minedu.gov.gr/ypapegan/anakoinoseis/59181-21-08-24-monimoi-diorismoi-6-211-ekpaideftikon-se-kenes-organikes-theseis-ekpaideftikon-protovathmias-kai-defterovathmias-eidikis-agogis-kai-ekpaidefsis-kai-genikis-ekpaidefsis-se-efarmogi-ton-diatakseon-tou-arthrou-62-tou-n-4589-2019-a-13)


## ΠΙΝΑΚΕΣ 2ΓΕ

2026 - https://info.asep.gr/node/78701
2023 - https://info.asep.gr/node/62781
2019 - https://info.asep.gr/node/62711

## ΠΙΝΑΚΕΣ 2ΕΑ

2025 - https://info.asep.gr/node/76177