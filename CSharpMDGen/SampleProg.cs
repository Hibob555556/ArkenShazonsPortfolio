using System;
using System.Collections.Generic;

/// <summary>
/// Represents an item in the inventory.
/// </summary>
public class InventoryItem
{
    /// <summary>
    /// The unique identifier of the item.
    /// </summary>
    public int Id { get; set; }

    /// <summary>
    /// The name of the inventory item.
    /// </summary>
    public string Name { get; set; }

    /// <summary>
    /// The quantity in stock.
    /// </summary>
    public int Quantity { get; set; }

    /// <summary>
    /// Indicates whether the item is active.
    /// </summary>
    public bool IsActive { get; set; }

    public InventoryItem(int id, string name, int quantity, bool isActive = true)
    {
        Id = id;
        Name = name;
        Quantity = quantity;
        IsActive = isActive;
    }

    public override string ToString()
    {
        return $"{Name} (ID: {Id}) - Qty: {Quantity} - Active: {IsActive}";
    }
}

/// <summary>
/// Manages the inventory for the system.
/// </summary>
public class InventoryManager
{
    private readonly List<InventoryItem> _items = new();

    /// <summary>
    /// Adds a new item to the inventory.
    /// </summary>
    public void AddItem(InventoryItem item)
    {
        _items.Add(item);
    }

    /// <summary>
    /// Removes an item by ID.
    /// </summary>
    public bool RemoveItem(int id)
    {
        var item = _items.Find(i => i.Id == id);
        if (item != null)
        {
            _items.Remove(item);
            return true;
        }
        return false;
    }

    /// <summary>
    /// Lists all active items in the inventory.
    /// </summary>
    public void ListActiveItems()
    {
        Console.WriteLine("Active Inventory Items:");
        foreach (var item in _items)
        {
            if (item.IsActive)
                Console.WriteLine(item);
        }
    }
}
