CREATE PROCEDURE `sp_isAttending`(
	IN p_user_id BIGINT,
    IN p_event_id BIGINT
)
BEGIN
	SELECT CASE WHEN EXISTS (
		SELECT UE.id
		FROM user_event UE
		WHERE UE.id = p_user_id AND
			UE.event_id = p_event_id
	)
	THEN 'TRUE'
	ELSE 'FALSE'
	END;
END