CREATE PROCEDURE `sp_getAllEvents` (
	IN p_date DATE
)
BEGIN
	SELECT * FROM `event`
    WHERE event_date > p_date;

END