import psycopg2

connection = psycopg2.connect(host='fw.payco.net.ve', database='luka_calidad', user='rmadonna', password='6WLb@R^WNCXSeE', port =  54320)

cursor = connection.cursor()

hola = """ 
select distinct t.id as "Id", t.id_traza, t.codigo_autorizacion, t.ip, c.nombre as "Canal", s.nombre as "Servicio",t.fecha_creacion at time zone 'vet' as "Fecha",
t.fecha_modificacion at time zone 'vet' as "Fecha Modificacion",
mon.codigo as "Moneda", t.monto as "Monto",
t.email_tarjetahabiente as "Email", t.nombre_pagador as "Nombre", e.descripcion as "Estatus",
m.nombre_comercial as "Marca", su.nombre_comercial as "Sucursal", mer.nombre as merchant, t.tarjeta, t.tipo_tarjeta,
tp.nombre as "Tipo Pago",
ml.codigo as "Moneda", replace(t.monto_usd::text,'.',',') as "Abono",
p.nombre as "Pais",
t.descripcion as "Descripcion",
c.nombre as "Canal",
t.respuesta_bluesnap as "Respuesta Bluesnap",
t.observaciones as "Observaciones",
concat(u.nombre, ' ', u.apellido) as aprobado_por,
CASE WHEN t.id_usuario_marca_aprobacion is null AND t.id_estatus in (6,7) THEN 'automática' ELSE 'manual' END tipo_aprobacion
from transaccion t
inner join servicio s on s.id=t.id_servicio
inner join estatus e on e.id=t.id_estatus
inner join pais p  on p.id=t.id_pais
inner join sucursal su on su.id=s.id_sucursal
inner join marca m on m.id=su.id_marca
inner join moneda mon on mon.id=t.id_moneda
inner join moneda ml on t.id_moneda_liquidacion=ml.id
inner join merchant mer on mer.id=t.id_merchant
inner join tipo_pago tp on tp.id=t.id_tipo_pago
inner join canal c on c.id=t.id_canal
left join usuario_marca u on t.id_usuario_marca_aprobacion=u.id
where mer.clave='tdc_bs'
and t.fecha_creacion at time zone 'vet' between '2023-01-01 00:00:00' and '2023-12-31 23:59:59'
order by 7 desc
limit 1
"""

cursor.execute(hola)
for query in cursor:
    print (query)
