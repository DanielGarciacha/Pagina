-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-07-2024 a las 04:08:24
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `proyecto`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `citas`
--

CREATE TABLE `citas` (
  `id` int(11) NOT NULL,
  `estudiante_id` int(11) DEFAULT NULL,
  `psicologo_id` int(11) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `hora` time DEFAULT NULL,
  `motivo` text DEFAULT NULL,
  `estado` varchar(50) DEFAULT 'pendiente'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recomendaciones_enfermeria`
--

CREATE TABLE `recomendaciones_enfermeria` (
  `id` int(11) NOT NULL,
  `medico_id` int(11) DEFAULT NULL,
  `estudiante_id` int(11) DEFAULT NULL,
  `recomendacion` text DEFAULT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `identificacion` varchar(15) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `funcion` varchar(20) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `rol` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `user`
--

INSERT INTO `user` (`id`, `nombre`, `identificacion`, `correo`, `telefono`, `funcion`, `username`, `password`, `rol`) VALUES
(1, 'David bastos', '12345678', 'dbasto@unibarranquilla.edu.co', '300000', 'Administrador', 'admin1', 'admin1', 'admin1'),
(2, 'Daniel Garcia', '987654321', 'dmanbuelgarcia@unibarraqnuilla.edu.co', '34000000', 'Administrador', 'admin2', 'admin2', 'admin2'),
(3, 'Saray Garcia', '1357911', 'saraygarcia@unibarramquilla.edu.co', '200000', 'Enfermera', 'emfermera1', 'enfermera1', 'emfermera1'),
(4, 'Edwin garcia', '879648', 'egarcia@unibarranquilla.edu.co', '30000000', 'psicologo', 'psicogo1', 'psicologo1', 'psicologo1'),
(5, 'Julian Garcia ', '1130267875', 'jgarcia@unibarranquilla.eedu.co', '3000290', 'Estudiante', 'Estudiante1', 'Estudiante1', 'Estudiante1');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `citas`
--
ALTER TABLE `citas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `estudiante_id` (`estudiante_id`),
  ADD KEY `psicologo_id` (`psicologo_id`);

--
-- Indices de la tabla `recomendaciones_enfermeria`
--
ALTER TABLE `recomendaciones_enfermeria`
  ADD PRIMARY KEY (`id`),
  ADD KEY `medico_id` (`medico_id`),
  ADD KEY `estudiante_id` (`estudiante_id`);

--
-- Indices de la tabla `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `citas`
--
ALTER TABLE `citas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `recomendaciones_enfermeria`
--
ALTER TABLE `recomendaciones_enfermeria`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `citas`
--
ALTER TABLE `citas`
  ADD CONSTRAINT `citas_ibfk_1` FOREIGN KEY (`estudiante_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `citas_ibfk_2` FOREIGN KEY (`psicologo_id`) REFERENCES `user` (`id`);

--
-- Filtros para la tabla `recomendaciones_enfermeria`
--
ALTER TABLE `recomendaciones_enfermeria`
  ADD CONSTRAINT `recomendaciones_enfermeria_ibfk_1` FOREIGN KEY (`medico_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `recomendaciones_enfermeria_ibfk_2` FOREIGN KEY (`estudiante_id`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
