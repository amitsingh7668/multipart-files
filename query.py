SELECT 
    TO_CHAR(TO_TIMESTAMP(REQUESTDATE, 'YYYY-MM-DD"T"HH24:MI:SS.FF3'), 'YYYY-MM-DD') AS request_day,
    COUNT(*) AS total_requests,
    SUM(CASE WHEN isActive = 1 THEN 1 ELSE 0 END) AS tickets_still_open,
    SUM(CASE WHEN isActive = 0 THEN 1 ELSE 0 END) AS tickets_closed,
    (SELECT COUNT(*) 
     FROM ETS_T_METADATA sub
     WHERE isActive = 0 
       AND REGEXP_LIKE(CLOSEDATE, '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?$')
       AND TO_CHAR(TO_TIMESTAMP(CLOSEDATE, 'YYYY-MM-DD"T"HH24:MI:SS.FF3'), 'YYYY-MM-DD') = TO_CHAR(TO_TIMESTAMP(main.REQUESTDATE, 'YYYY-MM-DD"T"HH24:MI:SS.FF3'), 'YYYY-MM-DD')
    ) AS tickets_closed_on_day
FROM 
    ETS_T_METADATA main
WHERE 
    REGEXP_LIKE(REQUESTDATE, '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?$')
    AND TO_TIMESTAMP(REQUESTDATE, 'YYYY-MM-DD"T"HH24:MI:SS.FF3') >= SYSDATE - 10
GROUP BY 
    TO_CHAR(TO_TIMESTAMP(REQUESTDATE, 'YYYY-MM-DD"T"HH24:MI:SS.FF3'), 'YYYY-MM-DD')
ORDER BY 
    request_day;
