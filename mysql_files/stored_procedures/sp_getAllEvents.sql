CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_getAllEvents`(
	IN p_date DATE
)
BEGIN
	SELECT event_id, event_name, event_city, DATE(event_date)  
    FROM `event`
    WHERE event_date > p_date;

END