CREATE PROCEDURE `sp_getUserEvent`(
    IN p_user_id BIGINT,
    IN p_date DATE
)
BEGIN
	SELECT event_id, event_name, event_city, DATE(event_date) 
    FROM `event` 
    WHERE event_date > p_date AND
		event_id IN
		(
			SELECT event_id FROM user_event
            WHERE id = p_user_id
        );

END