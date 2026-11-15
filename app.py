from flask import Flask, jsonify, request

app = Flask(__name__)

import Registro

#Endpoint 1: Perfil General (solo información básica)
@app.route("/api/perfil/<int:id>", method=["GET"])
def ver_perfil(id):
	#Buscamos el usuario por su ID en la colección local
	usuario = next((u for u in BASE_DATOS if u["id"] == id), None)

	if not usuario:
		return jsonify({"error": "Recurso no encontrado"}), 404

	#Minimización de datos: Exluimos 'condición de salud' deliberadamente
	perfil_filtrado = {
		"id": usuario["id"],
		"nombre": usuario["nombre"],
		"correo": usuario["correo"],
		"grupo": usuario["grupo"],
	}
	return jsonify(perfil_filtrado), 200



#Endpoint 2: Expediente (incluye información sensible)
@app.route("/api/expediente/<int:id>", methods=["GET"])
def ver_expedientes(id):
	usuario = next((u for u in BASE_DATOS if u["id"] == id), None)

	if not usuario:
		return jsonify({"error": "Recurso no encontrado"}), 404

	'''
	Este endpoint devuelve el registro completo (incluyendo "condicion_salud")
	'''
	expediente = {
		"id": usuario["id"],
		"nombre": usuario["nombre"],
		"correo": usuario["correo"],
		"grupo": usuario["grupo"],
		"condicion_salud": usuario["condicion_salud"],
	}
	return jsonify(expediente), 200

if __name__ == "__main__":
	app.run(debud=True, port=5000)
