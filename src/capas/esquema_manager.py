from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class EsquemaManager(BaseDatabaseSchemaEditor):

    def eliminar_columna(self, modelo, campo):
        sql = self.sql_delete_column % {
            "table": self.quote_name(modelo._meta.db_table),
            "column": self.quote_name(campo),
        }
        self.execute(sql)

    def agregar_columna(self, modelo, campo):
        definicion, params = self.column_sql(modelo, campo, include_default=True)
        sql = self.sql_create_column % {
            "table": self.quote_name(modelo._meta.db_table),
            "column": campo.db_column,
            "definition": definicion,
        }
        self.execute(sql, params)

    def editar_columna(self, modelo, anterior, nuevo, tipo):
        if anterior != nuevo:
            params = {
                        "table": self.quote_name(modelo._meta.db_table),
                        "old_column": anterior,
                        "new_column": nuevo
                    }
            if tipo is not None:
                params["type"] = tipo
            sql = self.sql_rename_column % params
            self.execute(sql)