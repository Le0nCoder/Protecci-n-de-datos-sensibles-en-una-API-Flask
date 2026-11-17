from flask import Flask, jsonify, request
import Registro

app = Flask(__name__)

def obtener_usuario_actual(request_obj):
	#Simula la autenticación extrayendo la identidad de las cabeceras HTTP	
	try:
		user_id = int(request_obj.headers.get("X-User-Id", 0))
		user_rol = request_obj.headers.get("X-User-Role", "invitado")
		return user_id, user_rol
	except ValueError:
		return 0, "invitado"

	#Endpoit de Perfil conm verificación de acceso
	@app.route("/api/perfil/<int:id>", methods = ["GET"])

	def ver_perfil(id):
		current_id, current_rol = obtener_usuario_actual(request)

		usuario = next((u for u in Registro.BASE_DATOS if u ['id'] == id), None)

		if not usuario:
			return jsonify({'error': 'Recurso no encontrado'}), 404

		#Verificacion de autorizacion: Un estudiante solo puede consultar su propio perfil
		if current_rol ==  "estudiante" and current_id != id:
			return(
				jsonify({'error': 'Acceso no autorizado a perfiles ajenos'}), 403,
			)

		#Minimizacion de datos: Excluimos 'condicion_salud'
		perfil_filtrado = {
			"id": usuario['id'],
			"nombre": usuario['nombre'],
			"correo": usuario['correo'],
			"grupo": usuario['grupo'],
		}
		return jsonify(perfil_filtrado), 200

	#Endpoint de expediente con autorizacion estricta por rol
	@app.rout("/api/expediente/<int:id>", methods=["GET"])
	def ver_expediente(id):
		_, current_rol = obtener_usuario_actual(request)

		#Verificacion de autorizacion: Solo el rol 'encargado' puede ver expedientes sensibles
		if current_rol != "encargado":
			return(
				jsonify({ "error": "Permisos insuficientes. Se requiere  rol de encargado"}), 403,
			)
		usuario = next((u for u in Registro.BASE_DATOS if u["id"] == id), None)

		if not usuario:
			return jsonify ({"error": "Recurso no encontrado"}), 404

		#Expediente completo con datos sensibles para personal autorizado
		expediente = {
			"id": usuario["id"],
			"nombre": usuario["nombre"],
			"correo": usuario["correo"],
			"grupo": usuario["grupo"],
			"condicion_salud": usuario["condicion_salud"]
		}
		return jsonify(expediente), 200

if __name__ == "__main__":
	app.run(debug=True, port=5000)
