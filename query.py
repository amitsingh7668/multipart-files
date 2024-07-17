WITH RequestData AS (
    SELECT
        TO_CHAR(TO_TIMESTAMP(REQUESTDATE, 'YYYY-MM-DD"T"HH24:MI:SS.FF3'), 'YYYY-MM-DD') AS request_day,
        isActive
    FROM 
        ETS_T_METADATA
    WHERE 
        REGEXP_LIKE(REQUESTDATE, '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?$')
        AND TO_TIMESTAMP(REQUESTDATE, 'YYYY-MM-DD"T"HH24:MI:SS.FF3') >= SYSDATE - 10
),
CloseData AS (
    SELECT
        TO_CHAR(TO_TIMESTAMP(CLOSEDATE, 'YYYY-MM-DD"T"HH24:MI:SS.FF3'), 'YYYY-MM-DD') AS close_day
    FROM 
        ETS_T_METADATA
    WHERE 
        REGEXP_LIKE(CLOSEDATE, '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?$')
        AND TO_TIMESTAMP(CLOSEDATE, 'YYYY-MM-DD"T"HH24:MI:SS.FF3') >= SYSDATE - 10
)
SELECT
    r.request_day,
    COUNT(*) AS total_requests,
    SUM(CASE WHEN r.isActive = 1 THEN 1 ELSE 0 END) AS tickets_still_open,
    SUM(CASE WHEN r.isActive = 0 THEN 1 ELSE 0 END) AS tickets_closed,
    COALESCE(c.total_closed, 0) AS total_closed_on_day
FROM 
    RequestData r
LEFT JOIN (
    SELECT
        close_day,
        COUNT(*) AS total_closed
    FROM 
        CloseData
    GROUP BY 
        close_day
) c
ON r.request_day = c.close_day
GROUP BY 
    r.request_day, c.total_closed
ORDER BY 
    r.request_day;

