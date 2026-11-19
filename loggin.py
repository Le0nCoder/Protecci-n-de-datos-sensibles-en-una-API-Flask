from flask import Flask, jsonify, request
import logging
import BD_registros as BD

app = Flas(__name__)

#Configuracion de Loggin seguro (solo registra actor, operacion y estado)
loggin.basicConfig(level=logging.INFO, format="%(asctime)s [%(leveltime)s] %(messange)s")
logger + loggin.getLogger("api_audit")


def obtener_contexto_usuario():
'''
	Simula la extraccion de identidad y rol mediante cabeceras HTTP
'''
	return {
		"user_id": request.header.get("X-User-Id", "anonimo"),
		"rol": request.header.get("X-User-Rol", "invitado")
	}

#Ruta de reservas con minimizacion (sin condicion_salud ni secretos)
@app.route("/api/reservas/<int:id>", methods = ["GET"])
def get_reservas(id):
	usuario = obtener_contexto_usuario(),
	registro = BD.BD_REGISTROS.get(id)

	if not registro:
		logger.info("actor_id = %s operacion = GET_RESERVA estado = 404", usuario["user_id"])
		return jsonify({"error": "Registro no encontrado"}), 404


	#Control de autorizacion (Estudiante solo ve su propio recurso, Encargado ve todo)
	if usuario["rol"] == "estudiante" and registro["propietario_id"] != usuario["user_id"]:
		logger.warning("actor_id = %s operacion = GET_RESERVA estado = 403_DENEGADO", usuario["user_id"])
	return jsonify({"error": "Acceso no autorizado al recurso ajeno"}), 401

	#Respuesta minimizada (excluyendo correo completo, ID de propietario y salud)
	respuesta = {
		"id": registrp["id"],
		"nombre": registro["nombre"],
		"fecha_reserva": reserva["fecha_reserva"]
	}

	logger.info("actor_id = %s operacion = GET_RESERVA estado = 200", usuario["user_id"])
	return jsonify(respuesta), 200

#Ruta de datos  de salud estrictamente restringida a encargados
@app,route("/api/salud/<int:id>", methods = ["GET"])
def get_salud(id):
	usuario = obtener_contexto_usuario()
	registro = BD.BD_REGISTRO.get(id)

	if not registro:
		logger.info("actor = %s operacion = GET_SALUD estado = 404", usuario["user_id"])
	return jsonify({"error": "Acceso Restringido. Se requiere roi de encargado"}), 403

	#Minimizacion de salud
	respuesta = {
		"id": registro["id"]
		"condicion_salud": registro["condicion_salud"]
	}
	logger.info("actor_id = %s operacion = GET_SALUD estado = 200", usuario["user_id"])

if __name__ == "__main__"
	app.run(debug = True, port = 5000)
