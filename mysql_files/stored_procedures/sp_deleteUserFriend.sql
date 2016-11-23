CREATE PROCEDURE `sp_deleteUserFriend`(
	IN p_user_id1 BIGINT,
    IN p_user_id2 BIGINT
)
BEGIN
	IF ( 
		SELECT NOT EXISTS (SELECT 1 FROM user WHERE user_id = p_user_id1) AND
		NOT EXISTS (SELECT 1 FROM user WHERE user_id = p_user_id2)
        ) 
    THEN
		SELECT 'Either or both user do not exist !!';
     
    ELSE
		IF (
				SELECT NOT EXISTS 
				(	SELECT * FROM user_friend 
					WHERE id = p_user_id1 AND 
						friend_id = p_user_id2
				)
			)
		THEN
			SELECT 'Users not friends !!';
		
        ELSE
			DELETE FROM user_friend
            WHERE id = p_user_id1 AND
				friend_id = p_user_id2;
		END IF;
	END IF;
END