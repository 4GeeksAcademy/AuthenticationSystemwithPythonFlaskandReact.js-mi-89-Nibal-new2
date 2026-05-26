import React from "react"
import { useNavigate } from "react-router-dom"

export const Home = () => {
	const navigate = useNavigate()
	const token = localStorage.getItem("token")

	React.useEffect(() => {
		if (!token) {
			navigate("/login")
		}
	}, [token, navigate])

	return (
		<div className="text-center mt-5">
			<h1>Welcome!</h1>
			<p>You are logged in</p>
		</div>
	)
}
