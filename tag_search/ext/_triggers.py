"""
WORK IN PROGRESS!!!!!
NOT USE IN PRODUCTION!!!!
"""

#from sqlalchemy.orm import sessionmaker
#from sqlalchemy import DDL
#
#postgresDDL = DDL("""
#set users.id to '1';
#
#CREATE OR REPLACE FUNCTION insert_data() RETURNS trigger AS $emp_stamp$ BEGIN NEW.create_at = now();
#NEW.update_at = now();
#NEW.id_create = current_setting('users.id', true);
#NEW.id_update = current_setting('users.id', true);
#IF NEW.id_create is null
#or NEW.id_update is null then RAISE EXCEPTION 'user is not defined!';
#END IF;
#RETURN NEW;
#END;
#$emp_stamp$ LANGUAGE plpgsql;
#CREATE OR REPLACE FUNCTION update_data() RETURNS trigger AS $emp_stamp$ begin NEW.id_create = OLD.id_create;
#NEW.create_at = OLD.create_at;
#NEW.update_at = now();
#NEW.id_update = current_setting('users.id', true);
#IF NEW.id_create is null
#or NEW.id_update is null then RAISE EXCEPTION 'user is not defined!';
#END IF;
#return NEW;
#END;
#$emp_stamp$ LANGUAGE plpgsql;
#
#create index index_users_id_users on users (id_users);
#create index index_users_nick_pass_is_admin on users (email, password, is_admin);
#create trigger trigger_users_insert before
#insert on users FOR EACH ROW EXECUTE PROCEDURE insert_data();
#create trigger trigger_users_update before
#update on users FOR EACH ROW EXECUTE PROCEDURE update_data();
#
#create index index_place_id_place on places (id_places);
#create trigger trigger_place_insert before
#insert on places FOR EACH ROW EXECUTE PROCEDURE insert_data();
#create trigger trigger_place_update before
#update on places FOR EACH ROW EXECUTE PROCEDURE update_data();
#
#create index index_tag_id_tag on tags (id_tags);
#create unique index index_unique_tag_name on tags (name);
#create trigger trigger_tag_insert before
#insert on tags FOR EACH ROW EXECUTE PROCEDURE insert_data();
#create trigger trigger_tag_update before
#update on tags FOR EACH ROW EXECUTE PROCEDURE update_data();
#
#create index index_place on placeags (id_places);
#create unique index index_place_tag on placeags (id_places, id_tags);
#
#create index index_messages_id_messages on messages (id_messages);
#create index index_messages_expire_date on messages (expire_date);
#create trigger trigger_messages_insert before
#insert on messages FOR EACH ROW EXECUTE PROCEDURE insert_data();
#create trigger trigger_messages_update before
#update on messages FOR EACH ROW EXECUTE PROCEDURE update_data();
#create trigger trigger_users_insert before
#insert on placeags FOR EACH ROW EXECUTE PROCEDURE insert_data();
#create trigger trigger_users_update before
#update on placeags FOR EACH ROW EXECUTE PROCEDURE update_data();
#    """
#)
#
#
#Session = sessionmaker(bind=db)
#session = Session()
#base.metadata.create_all(db)