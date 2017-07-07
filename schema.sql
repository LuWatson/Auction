drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  my integer not null,
  make text not null,
  model text not null,
  trim text not null,
  body_style text not null,
  drivetrain text not null,
  transmission text not null,
  vin CHAR(17) not null,
  mileage not null,
);
