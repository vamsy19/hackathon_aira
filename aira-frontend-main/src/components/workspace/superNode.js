import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Select, MenuItem, InputLabel, FormControl } from '@mui/material';
import {createSuperNode} from '../../services/api/layout';

const SuperNodeEditor = ({ nodes }) => {
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [entry, setEntry] = useState('');
    console.log(nodes);
    const handleSave = async () => {
        try {
            const superNodeData = {
                entry_node_id: entry,
                name,
                description
            };
            const data = await createSuperNode(superNodeData);
            console.log('Super node created:', data);
        } catch (error) {
            console.error('Error creating super node:', error);
        }
    };

    return (
        <Box sx={{ padding: 2 }}>
            <Typography variant="h5" gutterBottom>
                Create a Super Node
            </Typography>
            <TextField
                label="Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                fullWidth
                margin="normal"
                placeholder="Enter the name of the super node"
            />
            <TextField
                label="Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                fullWidth
                margin="normal"
                multiline
                rows={4}
                placeholder="Enter the description of the super node"
            />
            <FormControl fullWidth margin="normal">
                <InputLabel id="entry-label">Entry</InputLabel>
                <Select
                    labelId="entry-label"
                    value={entry}
                    onChange={(e) => setEntry(e.target.value)}
                    label="Entry"
                >
                    {nodes.map((node) => (
                        <MenuItem key={node.data.id} value={node.data.id}>
                            {node.data.name}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
            <Button variant="contained" color="primary" onClick={handleSave} sx={{ marginTop: 2 }}>
                Create
            </Button>
        </Box>
    );
};

export default SuperNodeEditor;
