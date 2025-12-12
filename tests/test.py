from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from datetime import datetime, timedelta

from airports.models import Airport, Route
from flights.models import AirplaneType, Airplane, Crew, Flight
from orders.models import Order, Ticket


class UserModelTest(TestCase):
    """Test suite for custom User model"""

    def setUp(self):
        self.user_data = {
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "User",
        }

    def test_create_user_with_email(self):
        """Test creating a user with email is successful"""
        user = get_user_model().objects.create_user(
            email=self.user_data["email"], password=self.user_data["password"]
        )

        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.check_password(self.user_data["password"]))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_user_email_normalized(self):
        """Test email is normalized for new users"""
        email = "test@EXAMPLE.COM"
        user = get_user_model().objects.create_user(email=email, password="test123")

        self.assertEqual(user.email, email.lower())

    def test_create_user_without_email_raises_error(self):
        """Test creating user without email raises ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email="", password="test123")

    def test_create_superuser(self):
        """Test creating a superuser"""
        admin = get_user_model().objects.create_superuser(
            email="admin@example.com", password="admin123"
        )

        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_user_str_representation(self):
        """Test the user string representation"""
        user = get_user_model().objects.create_user(
            email=self.user_data["email"], password=self.user_data["password"]
        )

        self.assertEqual(str(user), self.user_data["email"])


class AirportModelTest(TestCase):
    """Test suite for Airport model"""

    def setUp(self):
        self.airport_data = {
            "name": "John F. Kennedy International Airport",
            "closest_big_city": "New York",
        }

    def test_create_airport(self):
        """Test creating an airport is successful"""
        airport = Airport.objects.create(**self.airport_data)

        self.assertEqual(airport.name, self.airport_data["name"])
        self.assertEqual(
            airport.closest_big_city, self.airport_data["closest_big_city"]
        )

    def test_airport_str_representation(self):
        """Test the airport string representation"""
        airport = Airport.objects.create(**self.airport_data)
        expected_str = (
            f"{self.airport_data['name']} ({self.airport_data['closest_big_city']})"
        )

        self.assertEqual(str(airport), expected_str)

    def test_airports_ordering(self):
        """Test airports are ordered by name"""
        Airport.objects.create(name="Zulu Airport", closest_big_city="City Z")
        Airport.objects.create(name="Alpha Airport", closest_big_city="City A")
        Airport.objects.create(name="Beta Airport", closest_big_city="City B")

        airports = Airport.objects.all()
        self.assertEqual(airports[0].name, "Alpha Airport")
        self.assertEqual(airports[1].name, "Beta Airport")
        self.assertEqual(airports[2].name, "Zulu Airport")


class RouteModelTest(TestCase):
    """Test suite for Route model"""

    def setUp(self):
        self.source = Airport.objects.create(
            name="JFK Airport", closest_big_city="New York"
        )
        self.destination = Airport.objects.create(
            name="LAX Airport", closest_big_city="Los Angeles"
        )

    def test_create_route(self):
        """Test creating a route is successful"""
        route = Route.objects.create(
            source=self.source, destination=self.destination, distance=3944
        )

        self.assertEqual(route.source, self.source)
        self.assertEqual(route.destination, self.destination)
        self.assertEqual(route.distance, 3944)

    def test_route_str_representation(self):
        """Test the route string representation"""
        route = Route.objects.create(
            source=self.source, destination=self.destination, distance=3944
        )
        expected_str = f"{self.source} -> {self.destination} (3944 km)"

        self.assertEqual(str(route), expected_str)

    def test_routes_ordering(self):
        """Test routes are ordered by source and destination"""
        airport_a = Airport.objects.create(name="Airport A", closest_big_city="City A")
        airport_b = Airport.objects.create(name="Airport B", closest_big_city="City B")

        route1 = Route.objects.create(
            source=airport_b, destination=airport_a, distance=100
        )
        route2 = Route.objects.create(
            source=airport_a, destination=airport_b, distance=100
        )

        routes = Route.objects.all()
        self.assertEqual(routes[0], route2)


class AirplaneTypeModelTest(TestCase):
    """Test suite for AirplaneType model"""

    def test_create_airplane_type(self):
        """Test creating an airplane type"""
        airplane_type = AirplaneType.objects.create(name="Boeing 737")

        self.assertEqual(airplane_type.name, "Boeing 737")
        self.assertEqual(str(airplane_type), "Boeing 737")


class AirplaneModelTest(TestCase):
    """Test suite for Airplane model"""

    def setUp(self):
        self.airplane_type = AirplaneType.objects.create(name="Boeing 747")

    def test_create_airplane(self):
        """Test creating an airplane is successful"""
        airplane = Airplane.objects.create(
            name="BA-001", airplane_type=self.airplane_type, rows=30, seats_in_row=6
        )

        self.assertEqual(airplane.name, "BA-001")
        self.assertEqual(airplane.airplane_type, self.airplane_type)
        self.assertEqual(airplane.rows, 30)
        self.assertEqual(airplane.seats_in_row, 6)

    def test_airplane_capacity_calculation(self):
        """Test airplane capacity is calculated correctly"""
        airplane = Airplane.objects.create(
            name="BA-002", airplane_type=self.airplane_type, rows=25, seats_in_row=4
        )

        expected_capacity = 25 * 4
        self.assertEqual(airplane.capacity, expected_capacity)

    def test_airplane_str_representation(self):
        """Test the airplane string representation"""
        airplane = Airplane.objects.create(
            name="BA-003", airplane_type=self.airplane_type, rows=20, seats_in_row=6
        )
        expected_str = f"BA-003 ({self.airplane_type})"

        self.assertEqual(str(airplane), expected_str)


class CrewModelTest(TestCase):
    """Test suite for Crew model"""

    def test_create_crew_member(self):
        """Test creating a crew member"""
        crew = Crew.objects.create(first_name="John", last_name="Smith")

        self.assertEqual(crew.first_name, "John")
        self.assertEqual(crew.last_name, "Smith")

    def test_crew_str_representation(self):
        """Test the crew string representation"""
        crew = Crew.objects.create(first_name="Jane", last_name="Doe")

        self.assertEqual(str(crew), "Jane Doe")

    def test_crew_full_name_property(self):
        """Test the full_name property"""
        crew = Crew.objects.create(first_name="Alice", last_name="Johnson")

        self.assertEqual(crew.full_name, "Alice Johnson")


class FlightModelTest(TestCase):
    """Test suite for Flight model"""

    def setUp(self):
        self.source = Airport.objects.create(
            name="Source Airport", closest_big_city="Source City"
        )
        self.destination = Airport.objects.create(
            name="Destination Airport", closest_big_city="Destination City"
        )
        self.route = Route.objects.create(
            source=self.source, destination=self.destination, distance=1000
        )
        self.airplane_type = AirplaneType.objects.create(name="Airbus A320")
        self.airplane = Airplane.objects.create(
            name="AB-001", airplane_type=self.airplane_type, rows=30, seats_in_row=6
        )
        self.crew1 = Crew.objects.create(first_name="John", last_name="Pilot")
        self.crew2 = Crew.objects.create(first_name="Jane", last_name="Attendant")

    def test_create_flight(self):
        """Test creating a flight is successful"""
        departure = datetime.now()
        arrival = departure + timedelta(hours=2)

        flight = Flight.objects.create(
            departure_time=departure,
            arrival_time=arrival,
            airplane=self.airplane,
            route=self.route,
        )
        flight.crew.set([self.crew1, self.crew2])

        self.assertEqual(flight.airplane, self.airplane)
        self.assertEqual(flight.route, self.route)
        self.assertEqual(flight.crew.count(), 2)

    def test_flight_str_representation(self):
        """Test the flight string representation"""
        departure = datetime.now()
        arrival = departure + timedelta(hours=2)

        flight = Flight.objects.create(
            departure_time=departure,
            arrival_time=arrival,
            airplane=self.airplane,
            route=self.route,
        )

        expected_str = f"{self.route} ({departure})"
        self.assertEqual(str(flight), expected_str)

    def test_flights_ordering(self):
        """Test flights are ordered by departure time (descending)"""
        now = datetime.now()

        flight1 = Flight.objects.create(
            departure_time=now,
            arrival_time=now + timedelta(hours=2),
            airplane=self.airplane,
            route=self.route,
        )
        flight2 = Flight.objects.create(
            departure_time=now + timedelta(days=1),
            arrival_time=now + timedelta(days=1, hours=2),
            airplane=self.airplane,
            route=self.route,
        )

        flights = Flight.objects.all()
        self.assertEqual(flights[0], flight2)


class OrderModelTest(TestCase):
    """Test suite for Order model"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="customer@example.com", password="pass123"
        )

    def test_create_order(self):
        """Test creating an order is successful"""
        order = Order.objects.create(user=self.user)

        self.assertEqual(order.user, self.user)
        self.assertIsNotNone(order.created_at)

    def test_order_str_representation(self):
        """Test the order string representation"""
        order = Order.objects.create(user=self.user)

        self.assertIn(f"Order #{order.id}", str(order))
        self.assertIn(str(self.user), str(order))

    def test_orders_ordering(self):
        """Test orders are ordered by created_at (descending)"""
        order1 = Order.objects.create(user=self.user)
        order2 = Order.objects.create(user=self.user)

        orders = Order.objects.all()
        self.assertEqual(orders[0], order2)


class TicketModelTest(TestCase):
    """Test suite for Ticket model"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="customer@example.com", password="pass123"
        )
        self.order = Order.objects.create(user=self.user)

        self.source = Airport.objects.create(
            name="Airport A", closest_big_city="City A"
        )
        self.destination = Airport.objects.create(
            name="Airport B", closest_big_city="City B"
        )
        self.route = Route.objects.create(
            source=self.source, destination=self.destination, distance=500
        )

        self.airplane_type = AirplaneType.objects.create(name="Boeing 737")
        self.airplane = Airplane.objects.create(
            name="BA-123", airplane_type=self.airplane_type, rows=20, seats_in_row=6
        )

        departure = datetime.now()
        self.flight = Flight.objects.create(
            departure_time=departure,
            arrival_time=departure + timedelta(hours=2),
            airplane=self.airplane,
            route=self.route,
        )

    def test_create_ticket(self):
        """Test creating a ticket is successful"""
        ticket = Ticket.objects.create(
            order=self.order, flight=self.flight, row=5, seat=3
        )

        self.assertEqual(ticket.order, self.order)
        self.assertEqual(ticket.flight, self.flight)
        self.assertEqual(ticket.row, 5)
        self.assertEqual(ticket.seat, 3)

    def test_ticket_str_representation(self):
        """Test the ticket string representation"""
        ticket = Ticket.objects.create(
            order=self.order, flight=self.flight, row=5, seat=3
        )

        self.assertIn(f"Ticket #{ticket.id}", str(ticket))
        self.assertIn("Row 5", str(ticket))
        self.assertIn("Seat 3", str(ticket))

    def test_ticket_unique_together_constraint(self):
        """Test that same seat cannot be booked twice for same flight"""
        Ticket.objects.create(order=self.order, flight=self.flight, row=5, seat=3)

        with self.assertRaises(Exception):
            Ticket.objects.create(order=self.order, flight=self.flight, row=5, seat=3)

    def test_ticket_validation_row_exceeds_airplane_rows(self):
        """Test ticket validation fails when row exceeds airplane rows"""
        ticket = Ticket(order=self.order, flight=self.flight, row=21, seat=3)

        with self.assertRaises(ValidationError) as context:
            ticket.clean()
        self.assertIn("Row number cannot exceed 20", str(context.exception))

    def test_ticket_validation_seat_exceeds_seats_in_row(self):
        """Test ticket validation fails when seat exceeds seats_in_row"""
        ticket = Ticket(order=self.order, flight=self.flight, row=5, seat=7)

        with self.assertRaises(ValidationError) as context:
            ticket.clean()
        self.assertIn("Seat number cannot exceed 6", str(context.exception))

    def test_ticket_validation_valid_seat(self):
        """Test ticket validation passes for valid seat"""
        ticket = Ticket(order=self.order, flight=self.flight, row=10, seat=4)

        try:
            ticket.clean()
        except ValidationError:
            self.fail("Ticket validation raised ValidationError unexpectedly")

    def test_ticket_save_calls_clean(self):
        """Test that saving a ticket calls clean method"""
        ticket = Ticket(order=self.order, flight=self.flight, row=21, seat=3)

        with self.assertRaises(ValidationError) as context:
            ticket.save()
        self.assertIn("Row number cannot exceed 20", str(context.exception))


class ModelRelationshipTest(TestCase):
    """Test suite for model relationships"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="pass123"
        )
        self.source = Airport.objects.create(
            name="Airport A", closest_big_city="City A"
        )
        self.destination = Airport.objects.create(
            name="Airport B", closest_big_city="City B"
        )
        self.route = Route.objects.create(
            source=self.source, destination=self.destination, distance=500
        )
        self.airplane_type = AirplaneType.objects.create(name="Boeing 737")
        self.airplane = Airplane.objects.create(
            name="BA-001", airplane_type=self.airplane_type, rows=20, seats_in_row=6
        )
        departure = datetime.now()
        self.flight = Flight.objects.create(
            departure_time=departure,
            arrival_time=departure + timedelta(hours=2),
            airplane=self.airplane,
            route=self.route,
        )

    def test_airport_source_routes_relationship(self):
        """Test airport can access routes where it's the source"""
        routes = self.source.source_routes.all()
        self.assertEqual(routes.count(), 1)
        self.assertEqual(routes[0], self.route)

    def test_airport_destination_routes_relationship(self):
        """Test airport can access routes where it's the destination"""
        routes = self.destination.destination_routes.all()
        self.assertEqual(routes.count(), 1)
        self.assertEqual(routes[0], self.route)

    def test_route_flights_relationship(self):
        """Test route can access its flights"""
        flights = self.route.flights.all()
        self.assertEqual(flights.count(), 1)
        self.assertEqual(flights[0], self.flight)

    def test_airplane_flights_relationship(self):
        """Test airplane can access its flights"""
        flights = self.airplane.flights.all()
        self.assertEqual(flights.count(), 1)
        self.assertEqual(flights[0], self.flight)

    def test_user_orders_relationship(self):
        """Test user can access their orders"""
        order = Order.objects.create(user=self.user)
        orders = self.user.orders.all()
        self.assertEqual(orders.count(), 1)
        self.assertEqual(orders[0], order)

    def test_order_tickets_relationship(self):
        """Test order can access its tickets"""
        order = Order.objects.create(user=self.user)
        ticket = Ticket.objects.create(order=order, flight=self.flight, row=5, seat=3)
        tickets = order.tickets.all()
        self.assertEqual(tickets.count(), 1)
        self.assertEqual(tickets[0], ticket)

    def test_flight_tickets_relationship(self):
        """Test flight can access its tickets"""
        order = Order.objects.create(user=self.user)
        ticket = Ticket.objects.create(order=order, flight=self.flight, row=5, seat=3)
        tickets = self.flight.tickets.all()
        self.assertEqual(tickets.count(), 1)
        self.assertEqual(tickets[0], ticket)

    def test_crew_flights_relationship(self):
        """Test crew member can access flights they're assigned to"""
        crew = Crew.objects.create(first_name="John", last_name="Pilot")
        self.flight.crew.add(crew)

        flights = crew.flights.all()
        self.assertEqual(flights.count(), 1)
        self.assertEqual(flights[0], self.flight)
