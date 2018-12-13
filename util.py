import math

def escala_vetor_3d(v, escala):
	return [escala*v[0],escala*v[1],escala*v[2]]

def soma_vetor_3d(v1, v2):
	return [v1[0]+v2[0],v1[1]+v2[1],v1[2]+v2[2]]

def converter_esferica_r3(vetor_esferico, padding):
	r = vetor_esferico[0]
	cos_phi = math.cos(math.radians(vetor_esferico[1]))
	sin_phi = math.sin(math.radians(vetor_esferico[1]))
	cos_theta = math.cos(math.radians(vetor_esferico[2]))
	sin_theta = math.sin(math.radians(vetor_esferico[2]))

	x = r * sin_theta * cos_phi
	y = r * sin_theta * sin_phi
	z = r * cos_theta

	x += padding[0]
	y += padding[1]
	z += padding[2]

	return [x,y,z]