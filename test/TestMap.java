import Mapping.Map;
import Utils.Position;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class TestMap {

    @Test
    public void testMapConstructor() {
        Position pos_lower_left = new Position(-5, -5);
        Position pos_upper_right = new Position(5, 5);

        int width_calculated = (int)(10 / Map.SIZE_OF_CELL_IN_METER);
        int height_calculated = (int)(10 / Map.SIZE_OF_CELL_IN_METER);

        Map map = new Map(pos_lower_left, pos_upper_right);
        assertEquals(width_calculated, map.grid.length);
        assertEquals(height_calculated, map.grid[0].length);
    }

    @Test
    public void testMapPosition() {
        Map map = new Map(new Position(-2, -2), new Position(2, 2));
        Position pos_real_world = new Position(-1.9, 1.9);

        Position pos_in_map = map.toMapPosition(pos_real_world);

        assertEquals(0, pos_in_map.getXInt());
        assertEquals(0, pos_in_map.getYInt());
    }

    @Test
    void testMapPosition2() {
        Map map = new Map(new Position(-2, -2), new Position(2, 2));
        Position pos_real_world = new Position(0, 0);

        Position pos_in_map = map.toMapPosition(pos_real_world);

        assertEquals(4 / 2.0 / Map.SIZE_OF_CELL_IN_METER - 1, pos_in_map.getXInt());
        assertEquals(4 / 2.0 / Map.SIZE_OF_CELL_IN_METER - 1, pos_in_map.getYInt());
    }

    @Test
    void testWrongMapPosition() {
        Map map = new Map(new Position(-2, -2), new Position(2, 2));

        assertThrows(IllegalArgumentException.class, () -> map.toMapPosition(new Position(-5, 0)));
        assertThrows(IllegalArgumentException.class, () -> map.toMapPosition(new Position(5, 0)));
        assertThrows(IllegalArgumentException.class, () -> map.toMapPosition(new Position(0, -5)));
        assertThrows(IllegalArgumentException.class, () -> map.toMapPosition(new Position(0, 5)));
        assertDoesNotThrow(() -> map.toMapPosition(new Position(-2, -2)));
        assertDoesNotThrow(() -> map.toMapPosition(new Position(-2, 2)));
        assertDoesNotThrow(() -> map.toMapPosition(new Position(2, -2)));
        assertDoesNotThrow(() -> map.toMapPosition(new Position(2, 2)));


    }
}
