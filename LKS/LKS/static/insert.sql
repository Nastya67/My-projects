INSERT INTO comands VALUES
((SELECT array_to_string(ARRAY(SELECT chr((65 + round(random() * 25)) :: integer)
FROM generate_series(1,6)), '')), 'Странность Dance studio Luna', 0, 0, 'Amateur Juniors', 20),
('', 'NoName dance studio', 0, 0, 'Amateur Juniors', 21),
('', 'THE BOND', 0, 0, 'Amateur Juniors', 22),
('', 'LEADER DANCE', 0, 0, 'Amateur Juniors', 23),
('', 'Main Event Crew All Stars Dance Centre', 0, 0, 'Amateur Juniors', 24),
('', 'ART FUSION GANGSTA', 0, 0, 'Amateur Juniors', 25),
('', 'Жардин де ля Данс', 0, 0, 'Amateur Juniors', 26),
('', 'Future movement crew', 0, 0, 'Amateur Juniors', 27),
('', 'Dream Team (MAX DANCE)', 0, 0, 'Amateur Juniors', 28),
('', 'Diva dance Crew', 0, 0, 'Amateur Juniors', 29),
('', 'CREW WAY', 0, 0, 'Amateur Juniors', 30),
('', 'Kings of Chaos', 0, 0, 'Amateur Juniors', 31),
('', 'DSL Crew', 0, 0, 'Amateur Juniors', 32),
('', 'ART FUSION FAM', 0, 0, 'Amateur Juniors', 33),
('', 'Funky Fresh Crew (MAX DANCE)', 0, 0, 'Amateur Juniors', 34),
('', 'ANGELLAS CREW', 0, 0, 'Amateur Juniors', 35),
('', 'K.O.PAT', 0, 0, 'Amateur Juniors', 36),
('', 'Z-Royal', 0, 0, 'Amateur Juniors', 37),
('', 'One Beat Crew (Maxdance)', 0, 0, 'Amateur Juniors', 38),
('', 'Гравитация', 0, 0, 'Amateur Juniors', 39),
('', 'Banana crew', 0, 0, 'Amateur Juniors', 40),
('', 'Yes banda', 0, 0, 'Amateur Juniors', 41),
('', 'Dance for life', 0, 0, 'Amateur Juniors', 42),
('', 'Flying Stars', 0, 0, 'Amateur Juniors', 43),
('', 'Студия танца "Go Up"', 0, 0, 'Amateur Juniors', 44),
('', 'Brighting crew All Stars Dance Cantre', 0, 0, 'Amateur Juniors', 45),
('', 'Sup Team', 0, 0, 'Amateur Juniors', 46),
('', 'Princess', 0, 0, 'Amateur Juniors', 47),
('', 'Fresh Baking', 0, 0, 'Amateur Juniors', 48),
('', 'LatS go', 0, 0, 'Amateur Juniors', 49),
('', 'Lil Alphas', 0, 0, 'Amateur Juniors', 50),
('', 'Dance Family Spirit', 0, 0, 'Amateur Juniors', 51),
('', 'Soul Side', 0, 0, 'Amateur Juniors', 52),
('', 'Atom Dance Crew', 0, 0, 'Amateur Juniors', 53),
('', 'Soul flame', 0, 0, 'Amateur Juniors', 54);

INSERT INTO comands VALUES
('', 'RevolDance', 0, 0, 'Amateur Kids', 1),
('', 'Boys band', 0, 0, 'Amateur Kids', 2),
('', 'SHYK DANCE SHOW', 0, 0, 'Amateur Kids', 3),
('', 'Yummy crew', 0, 0, 'Amateur Kids', 4),
('', 'Живчик', 0, 0, 'Amateur Kids', 5),
('', 'Energy Kids', 0, 0, 'Amateur Kids', 6),
('', 'DSL Crew Dance Studio Luna', 0, 0, 'Amateur Kids', 7),
('', 'BONDДіти', 0, 0, 'Amateur Kids', 8),
('', 'Voronin`s Studio', 0, 0, 'Amateur Kids', 9),
('', 'Explosion Kids', 0, 0, 'Amateur Kids', 10),
('', 'Sharm-S Dolls', 0, 0, 'Amateur Kids', 11),
('', 'Flash Mob Dance Studio Luna', 0, 0, 'Amateur Kids', 12),
('', 'Грация', 0, 0, 'Amateur Kids', 13),
('', 'Блиц', 0, 0, 'Amateur Kids', 14),
('', 'ЦЕХ', 0, 0, 'Amateur Kids', 15),
('', 'Cartoon Kids', 0, 0, 'Amateur Kids', 16),
('', 'LetS go Kids', 0, 0, 'Amateur Kids', 17),
('', 'ART FUSION LITTLE MONSTERS', 0, 0, 'Amateur Kids', 18),
('', 'Dance Family Spirit', 0, 0, 'Amateur Kids', 19);

class judgment(FlaskForm):
    technique = wtforms.SelectField('Technique / Техника', choices=[(i, str(10-i/2)) for i in range(0, 21)], default=20)
    production = wtforms.SelectField('Direction / Постановка', choices=[(i, str(10-i/2)) for i in range(0, 21)], default=20)
    teamwork = wtforms.SelectField('Teamwork / Командная работа', choices=[(i, str(10-i/2)) for i in range(0, 21)], default=20)
    artistry = wtforms.SelectField('Artistry / Артистизм', choices=[(i, str(10-i/2)) for i in range(0, 21)], default=20)
    musicality = wtforms.SelectField('Musicality / Музыкальность', choices=[(i, str(10-i/2)) for i in range(0, 21)], default=20)
    show = wtforms.SelectField('Show / Шоу', choices=[(i, str(10-i/2)) for i in range(0, 21)], default=20)
    creativity = wtforms.SelectField('Creativity / Креативность', choices=[(i, str(10-i/2)) for i in range(0, 21)], default=20)
    submit = wtforms.SubmitField('OK')


INSERT INTO comands VALUES
('', 'DSN Community', 0, 0, 'Amateur Adults', 55),
('', 'Hallucinations UA21', 0, 0, 'Amateur Adults', 56),
('', 'Tagless', 0, 0, 'Amateur Adults', 57),
('', 'FDC fam', 0, 0, 'Amateur Adults', 58),
('', 'WAY UP CREW (MAX DANCE)', 0, 0, 'Amateur Adults', 59),
('', 'ARTPEOPLE CREW', 0, 0, 'Amateur Adults', 60),
('', 'All Stars Dance Centre команда Ice-D Crew', 0, 0, 'Amateur Adults', 61),
('', 'Coconut Union', 0, 0, 'Amateur Adults', 62),
('', 'TRIBUTE TEAM', 0, 0, 'Amateur Adults', 63),
('', 'Soul crew', 0, 0, 'Amateur Adults', 64),
('', 'A tale of the town', 0, 0, 'Amateur Adults', 65),
('', 'Blaze Up crew', 0, 0, 'Amateur Adults', 66),
('', 'All Stars Dance Centre команда Modern Madness', 0, 0, 'Amateur Adults', 67);

INSERT INTO comands VALUES
('', 'Juicyfruits', 0, 0, 'Pro Kids', 68),
('', 'DIVA Dance', 0, 0, 'Pro Kids', 69),
('', 'RDF', 0, 0, 'Pro Kids', 70),
('', 'Грация', 0, 0, 'Pro Kids', 71),
('', 'Freshies crew', 0, 0, 'Pro Kids', 72),
('', 'Step By Step Dance School', 0, 0, 'Pro Kids', 73),
('', 'Feel More Crew', 0, 0, 'Pro Kids', 74),
('', 'ТОРНАДО', 0, 0, 'Pro Kids', 75),
('', 'Apple kids', 0, 0, 'Pro Kids', 76),
('', 'Tagless', 0, 0, 'Pro Kids', 77);
