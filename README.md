# Zapatos Bernini

## Instalación
Prerequisitos
 - Python 3.6
 - Pipenv

```bash
git clone https://github.com/EnriqueSoria/ZapatosBernini.git && cd ZapatosBernini
pipenv sync
pipenv shell
python manage.py runserver
```

## Funcionalidades
### Panel de administración
La ruta del panel de administración es la estándar de Django: `/admin`
#### Como Administrador
 Usuario: `EnriqueSoria`
 Password: `enrique@cecotec`

 - Añadir, editar y borrar usuarios
    - Creación de usuarios, otorgando los permisos de `is_staff` y asignándolo al grupo `Customers`
 - Añadir, editar y borrar productos (`Items`)
 - Añadir, editar, borrar, descargar como csv y enviar pedidos (`Order`)
 
#### Como cliente
Usuario: `Customer 1`
Password: `customer@cecotec`

Usuario: `Customer 2`
Password: `customer@cecotec`

 - Ver productos (`Items`)
 - Añadir, editar, descargar como csv y enviar sus pedidos (`Orders`)
 
### API
Se puede acceder a la documentación en `/docs`
 - Ver la lista de productos y los detalles de estos
