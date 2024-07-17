WITH RequestData AS (
    SELECT
        TO_CHAR(TO_TIMESTAMP(m.REQUESTDATE, 'YYYY-MM-DD"T"HH24:MI:SS.FF3'), 'YYYY-MM-DD') AS request_day,
        m.isActive,
        m.workflow_id
    FROM 
        ETS_T_METADATA m
    WHERE 
        REGEXP_LIKE(m.REQUESTDATE, '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?$')
        AND TO_TIMESTAMP(m.REQUESTDATE, 'YYYY-MM-DD"T"HH24:MI:SS.FF3') >= SYSDATE - 10
),
CloseData AS (
    SELECT
        TO_CHAR(TO_TIMESTAMP(a.completedat, 'YYYY-MM-DD"T"HH24:MI:SS.FF3'), 'YYYY-MM-DD') AS close_day,
        a.metadata_id
    FROM 
        ETS_T_ACTION_ROLE a
    WHERE 
        a.Active = 0
        AND a.metadata_id IN (
            SELECT workflow_id
            FROM ETS_T_METADATA
        )
),
LatestCloseData AS (
    SELECT
        metadata_id,
        MAX(completedat) AS latest_completedat
    FROM
        ETS_T_ACTION_ROLE
    WHERE
        Active = 0
    GROUP BY
        metadata_id
)
SELECT
    r.request_day,
    COUNT(*) AS total_requests,
    SUM(CASE WHEN r.isActive = 1 THEN 1 ELSE 0 END) AS tickets_still_open,
    SUM(CASE WHEN r.isActive = 0 AND TO_CHAR(TO_TIMESTAMP(l.latest_completedat, 'YYYY-MM-DD"T"HH24:MI:SS.FF3'), 'YYYY-MM-DD') = r.request_day THEN 1 ELSE 0 END) AS tickets_closed_same_day,
    COALESCE((
        SELECT COUNT(*)
        FROM CloseData c
        WHERE c.close_day = r.request_day
    ), 0) AS total_closed_on_day
FROM 
    RequestData r
LEFT JOIN 
    LatestCloseData l ON r.workflow_id = l.metadata_id
GROUP BY 
    r.request_day
ORDER BY 
    r.request_day;
