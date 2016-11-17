CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addEvent`(
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
		INSERT INTO user_event
		(
			id,
			event_id
		)
		VALUES
		(
			p_user_id,
			p_event_id
		);
        
	END IF;
END