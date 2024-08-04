-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 21-07-2024 a las 05:12:54
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
-- Estructura de tabla para la tabla `citas_psicologia`
--

CREATE TABLE `citas_psicologia` (
  `id` int(11) NOT NULL,
  `nombre_apellidos` varchar(100) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `genero` enum('male','female','other') NOT NULL,
  `motivo` enum('ansiedad','depresion','estres','relaciones','autoestima','trauma','adicciones','desarrollo','academico','salud_mental','otros') NOT NULL,
  `fecha_reserva` date NOT NULL,
  `sede` enum('Barranquilla','Soledad') NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `enfermero`
--

CREATE TABLE `enfermero` (
  `id_enfermero` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `correo_institucional` varchar(50) NOT NULL,
  `identificacion` int(13) NOT NULL,
  `telefono` int(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiante`
--

CREATE TABLE `estudiante` (
  `id_estudiante` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `tipo_documento` enum('cc','ti') NOT NULL,
  `identificacion` int(13) NOT NULL,
  `telefono` int(15) DEFAULT NULL,
  `historial_clinico` mediumblob DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `psicologo`
--

CREATE TABLE `psicologo` (
  `id_psicologo` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `correo_institucional` varchar(50) NOT NULL,
  `identificacion` int(13) NOT NULL,
  `telefono` int(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recomendaciones_enfermeria`
--

CREATE TABLE `recomendaciones_enfermeria` (
  `id_recomendacion` int(11) NOT NULL,
  `id_enfermero` int(11) NOT NULL,
  `id_estudiante` int(11) NOT NULL,
  `fecha_recomendacion` date NOT NULL,
  `recomendacion` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recomendaciones_psicologia`
--

CREATE TABLE `recomendaciones_psicologia` (
  `id` int(11) NOT NULL,
  `id_psicologo` int(11) NOT NULL,
  `id_estudiante` int(11) NOT NULL,
  `recomendacion` text NOT NULL,
  `fecha` date NOT NULL
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
(5, 'Julian Garcia ', '1130267875', 'jgarcia@unibarranquilla.eedu.co', '3000290', 'Estudiante', 'Estudiante1', 'Estudiante1', 'Estudiante1'),
(6, 'juan ', '12345', 'example@example', '3000000', '', 'estudiante2', 'estudiante2', 'estudiante');

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
-- Indices de la tabla `citas_psicologia`
--
ALTER TABLE `citas_psicologia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `enfermero`
--
ALTER TABLE `enfermero`
  ADD PRIMARY KEY (`id_enfermero`),
  ADD KEY `id_user` (`id_user`);

--
-- Indices de la tabla `estudiante`
--
ALTER TABLE `estudiante`
  ADD PRIMARY KEY (`id_estudiante`),
  ADD KEY `id_user` (`id_user`);

--
-- Indices de la tabla `psicologo`
--
ALTER TABLE `psicologo`
  ADD PRIMARY KEY (`id_psicologo`),
  ADD KEY `id_user` (`id_user`);

--
-- Indices de la tabla `recomendaciones_enfermeria`
--
ALTER TABLE `recomendaciones_enfermeria`
  ADD PRIMARY KEY (`id_recomendacion`),
  ADD KEY `id_enfermero` (`id_enfermero`),
  ADD KEY `id_estudiante` (`id_estudiante`);

--
-- Indices de la tabla `recomendaciones_psicologia`
--
ALTER TABLE `recomendaciones_psicologia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_psicologo` (`id_psicologo`),
  ADD KEY `id_estudiante` (`id_estudiante`);

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
-- AUTO_INCREMENT de la tabla `citas_psicologia`
--
ALTER TABLE `citas_psicologia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `enfermero`
--
ALTER TABLE `enfermero`
  MODIFY `id_enfermero` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `estudiante`
--
ALTER TABLE `estudiante`
  MODIFY `id_estudiante` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `psicologo`
--
ALTER TABLE `psicologo`
  MODIFY `id_psicologo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `recomendaciones_enfermeria`
--
ALTER TABLE `recomendaciones_enfermeria`
  MODIFY `id_recomendacion` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `recomendaciones_psicologia`
--
ALTER TABLE `recomendaciones_psicologia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

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
-- Filtros para la tabla `citas_psicologia`
--
ALTER TABLE `citas_psicologia`
  ADD CONSTRAINT `citas_psicologia_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `enfermero`
--
ALTER TABLE `enfermero`
  ADD CONSTRAINT `enfermero_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `estudiante`
--
ALTER TABLE `estudiante`
  ADD CONSTRAINT `estudiante_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `psicologo`
--
ALTER TABLE `psicologo`
  ADD CONSTRAINT `psicologo_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `recomendaciones_enfermeria`
--
ALTER TABLE `recomendaciones_enfermeria`
  ADD CONSTRAINT `recomendaciones_enfermeria_ibfk_1` FOREIGN KEY (`id_enfermero`) REFERENCES `enfermero` (`id_enfermero`) ON DELETE CASCADE,
  ADD CONSTRAINT `recomendaciones_enfermeria_ibfk_2` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiante` (`id_estudiante`) ON DELETE CASCADE;

--
-- Filtros para la tabla `recomendaciones_psicologia`
--
ALTER TABLE `recomendaciones_psicologia`
  ADD CONSTRAINT `recomendaciones_psicologia_ibfk_1` FOREIGN KEY (`id_psicologo`) REFERENCES `psicologo` (`id_psicologo`) ON DELETE CASCADE,
  ADD CONSTRAINT `recomendaciones_psicologia_ibfk_2` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiante` (`id_estudiante`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
