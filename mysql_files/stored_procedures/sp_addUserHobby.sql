CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addUserHobby`(
	IN p_user_id BIGINT,
    IN p_hobby_id BIGINT
)
BEGIN
	IF ( 
		SELECT NOT EXISTS (SELECT 1 FROM user WHERE user_id = p_user_id) AND
		NOT EXISTS (SELECT 1 FROM hobby WHERE hobby_id = p_hobby_id)
        ) 
    THEN
		SELECT 'Either user or hobby or both do not exist !!';
     
    ELSE
		INSERT INTO user_hobby
		(
			id,
			hobby_id
		)
		VALUES
		(
			p_user_id,
			p_hobby_id
		);
        
	END IF;
END