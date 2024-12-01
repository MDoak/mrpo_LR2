--1
SELECT s."Name" FROM "Souvenirs" s 
JOIN "SouvenirMaterials" m ON s."IdMaterial" = m."ID" 
WHERE m."Name"  = 'бук'

--2
select s."Name", sp."Date"  from "Souvenirs" s 
join "ProcurementSouvenirs" ps ON s."ID" = ps."IdSouvenir" 
join "SouvenirProcurements" sp ON ps."IdProcurement" = sp."ID"
where sp."Date" between '2023-03-17' and '2024-04-01'

--3 
select s."Name", sc."Name" from "Souvenirs" s
join "SouvenirsCategories" sc on s."IdCategory"  = sc."ID"
where sc."Name" = 'Поло'
order by s."Rating" desc

--4 
select p."Name", sc."Name" from "Providers" p
join "SouvenirProcurements" sp on p."ID" =sp."IdProvider" 
join "ProcurementSouvenirs" ps on sp."ID" = ps."IdProcurement" 
join "Souvenirs" s on ps."IdSouvenir"  = s."ID"
join "SouvenirsCategories" sc on s."IdCategory" = sc."ID"
where sc."Name" = 'Куртки'

--5
select s."Name", sp."Date" from "Souvenirs" s 
join "ProcurementSouvenirs" ps ON s."ID" = ps."IdSouvenir" 
join "SouvenirProcurements" sp ON ps."IdProcurement" = sp."ID"
join "ProcurementStatuses" ps2 on sp."IdStatus" = ps2."ID" 
where sp."Date" between '2023-03-17' and '2024-04-01'
order by ps2."Name"

--6
create or replace function get_categories(int) returns setof "SouvenirsCategories" as $$
	select * from "SouvenirsCategories" sc where sc."IdParent" = $1;
$$ language sql;

select * from get_categories(3193)

--7
create or replace function check_catogories_insert()
	returns trigger
as $$
begin
	if new."Name" is null or new."Name" = '' then
		raise exception 'Incorrect filling field "Name"';
	end if;
	return new;
end;
$$ language plpgsql;

create trigger categories_trigger
before insert on "SouvenirsCategories"
for each row
execute procedure check_catogories_insert()

insert into "SouvenirsCategories" ("IdParent", "Name") 
values (1, '')

--8
create or replace function amount_warning()
	returns trigger 
as $$
begin
	if new."Amount" = 0 then
		if not exists (select "SouvenirStores"."IdSouvenir"  from "SouvenirStores"
					where "SouvenirStores"."IdSouvenir"  = new."IdSouvenir") then
			raise notice 'notice 1';
		end if;
	else
		if new."Amount" < 50 then
			raise notice 'notice 2';
		end if;
	end if;
	return new;
end;
$$ language plpgsql;

create trigger procurement_souvenir_trigger
after insert on "SouvenirStores"
for each row
execute procedure amount_warning()

insert into "SouvenirStores" ("IdSouvenir", "IdProcurement", "Amount", "Comments")
values (17682, 16, 2, 'Comment')
insert into "SouvenirStores" ("IdSouvenir", "IdProcurement", "Amount", "Comments")
values (8105, 16, 15, 'Comment')




	
