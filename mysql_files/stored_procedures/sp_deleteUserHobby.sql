CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_deleteUserHobby`(
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
		IF (
				SELECT NOT EXISTS 
				(	SELECT * FROM user_hobby 
					WHERE id = p_user_id AND 
						hobby_id = p_hobby_id
				)
			)
		THEN
			SELECT 'User does not have this hobby !!';
		
        ELSE
			DELETE FROM user_hobby
            WHERE id = p_user_id AND
				hobby_id = p_hobby_id;
		END IF;
	END IF;
END