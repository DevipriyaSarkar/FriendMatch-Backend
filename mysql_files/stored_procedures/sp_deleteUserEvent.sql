CREATE PROCEDURE `sp_deleteUserEvent`(
	IN p_user_id BIGINT,
    IN p_event_id BIGINT
)
BEGIN
	IF ( 
		SELECT NOT EXISTS (SELECT 1 FROM user WHERE user_id = p_user_id) AND
		NOT EXISTS (SELECT 1 FROM `event` WHERE event_id = p_event_id)
        ) 
    THEN
		SELECT 'Either user or event or both do not exist !!';
	
    ELSE
		IF (
				SELECT NOT EXISTS 
				(	SELECT * FROM user_event 
					WHERE id = p_user_id AND 
						event_id = p_event_id
				)
			)
		THEN
			SELECT 'User is not attending this event !!';
		
        ELSE
			DELETE FROM user_event
            WHERE id = p_user_id AND
				event_id = p_event_id;
		END IF;
	END IF;
END