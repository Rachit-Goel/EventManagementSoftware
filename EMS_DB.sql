use EMS_DB;

create table venue(
v_name varchar(25),
location varchar(25),
venue_id varchar(25) not null,primary key(venue_id));

create table client(
c_id varchar(25) not null,
payment_status varchar(25) not null DEFAULT 'UNPAID',
advance_payment  int not null default 2000,
total_payment  int not null default 0,
client_type varchar(25),primary key(c_id));

create table event(
event_id varchar(25) not null,
e_name varchar(25),
c_id varchar(25),
venue_id varchar(25),primary key(event_id),foreign key(venue_id) references venue(venue_id),foreign key(c_id) references client(c_id));

create table event_schedule(
e_date date,
e_start_time time not null,
venue_id varchar(25),
event_id varchar(25),
c_id varchar(25),primary key(e_start_time,e_date,venue_id),
e_description varchar(25) default "DESCRIPTION",
foreign key(venue_id) references venue(venue_id),foreign key(event_id) references event(event_id));

create table wedding_info(
c_id varchar(25) not null,
c_name varchar(25),primary key(c_id)
);

create table w_contact_details(
c_id varchar(25) not null,
 W_address varchar(25) not null default "Address",
 W_emailid varchar(25) not null default "example@gmail.com",
contact_No varchar(25) not null,primary key(contact_No,c_id),foreign key(c_id) references wedding_info(c_id)
);

create table seminar_info(
c_id varchar(25) not null,
c_name varchar(25),primary key(c_id)
);

create table s_contact_details(
c_id varchar(25) not null,
s_address varchar(25) not null default "Address",
s_emailid varchar(25) not null default "example@gmail.com",
contact_No varchar(25) not null,primary key(contact_No,c_id),foreign key(c_id) references seminar_info(c_id)
);

create table conference_info(
c_id varchar(25) not null,
c_name varchar(25),primary key(c_id)
);

create table c_contact_details(
c_id varchar(25) not null,
contact_No varchar(25) not null,primary key(contact_No,c_id),
 c_address varchar(25) not null default "Address",
 c_emailid varchar(25) not null default "example@gmail.com",
foreign key(c_id) references conference_info(c_id)
);

create table inventory(
 model_no varchar(25) not null,
 item_name varchar(25),
 event_id varchar(25) not null,
 primary key (model_no,event_id), foreign key(event_id) references event(event_id) );
 
create table staff( 
s_id varchar(25) not null,
 s_type varchar(25) ,
 primary key (s_id)  );
 
create table production_info (
 s_id varchar(25) not null,
 p_name varchar(25), 
 primary key (s_id),
 foreign key(s_id) references staff(s_id) );
 
create table catering_info ( 
s_id varchar(25) not null,
 ca_name varchar(25),
 primary key (s_id), foreign key(s_id) references staff(s_id) );

create table ca_salary_details ( 
contact_no int not null, 
salary int, 
primary key (contact_no));
 
create table ca_contact_details ( 
  contact_no int not null,
 s_id varchar(25) not null,
 ca_address varchar(25) not null default "Address",
 ca_emailid varchar(25) not null default "example@gmail.com",
 primary key (contact_no,s_id),
 foreign key(contact_no) references ca_salary_details(contact_no), foreign key(s_id) references catering_info(s_id) );
 
create table p_salary_details ( contact_no int not null, 
salary int, 
primary key (contact_no)
);
  
create table p_contact_details ( contact_no int not null, 
s_id varchar(25) not null, 
primary key (contact_no,s_id),
p_address varchar(25) not null  default "Address",
p_emailid varchar(25) not null  default "example@gmail.com", 
foreign key(contact_no) references p_salary_details(contact_no), 
foreign key(s_id) references production_info(s_id)  
 );

create table Users(
u_id varchar(25) not null,
user_name varchar(25) not null,
user_designation varchar(25) not null,
user_password varchar(25) not null,
user_contact_no int not null,
user_address varchar(25) not null,
primary key(u_id));


